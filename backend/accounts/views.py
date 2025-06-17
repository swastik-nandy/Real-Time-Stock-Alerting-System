from django.shortcuts import redirect
from django.contrib.auth import login, logout
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings

import os
import json

from .forms import CustomUserCreationForm, CustomAuthenticationForm, ForgotPasswordForm
from .models import CustomUser, PasswordResetOTP
from .utils import generate_otp
from alerts.models import Alert
from stocks.models import Stock

from rest_framework_simplejwt.tokens import RefreshToken
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests

# -------------------- Register --------------------

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return JsonResponse({
                'status': 'registered',
                'user': {
                    'email': user.email,
                    'username': user.username,
                    'full_name': user.full_name
                }
            })
        return JsonResponse({'errors': form.errors}, status=400)
    return JsonResponse({'error': 'GET not allowed'}, status=405)

# -------------------- Native Login --------------------

def login_view(request):
    form = CustomAuthenticationForm(request, data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.get_user()
            if user.is_superuser or user.is_staff:
                return JsonResponse({'error': "Admin users cannot login from here."}, status=403)
            login(request, user)
            return JsonResponse({
                'status': 'logged in',
                'user': {
                    'email': user.email,
                    'username': user.username,
                    'full_name': user.full_name
                }
            })
        return JsonResponse({'error': "Invalid email or password."}, status=401)
    return JsonResponse({'error': 'GET not allowed'}, status=405)

# -------------------- Google OAuth Login via React --------------------

@csrf_exempt
def google_login_view(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'GET not allowed'}, status=405)

    try:
        body = json.loads(request.body)
        token = body.get('token')
        print("🔍 Received token:", token)

        if not token:
            return JsonResponse({'error': 'Missing token'}, status=400)

        # ✅ Attempt token verification with retry on early token error
        try:
            idinfo = id_token.verify_oauth2_token(
                token,
                google_requests.Request(),
                audience="771864820870-6gr9tvifa16im1cbi3sdc3dluop5f1k7.apps.googleusercontent.com"
            )
        except ValueError as ve:
            if 'Token used too early' in str(ve):
                print("⚠️ Token used too early — retrying after 1 second...")
                import time
                time.sleep(1)
                idinfo = id_token.verify_oauth2_token(
                    token,
                    google_requests.Request(),
                    audience="771864820870-6gr9tvifa16im1cbi3sdc3dluop5f1k7.apps.googleusercontent.com"
                )
            else:
                print("❌ Token verification failed:", ve)
                return JsonResponse({'error': 'Invalid Google token'}, status=400)

        email = idinfo.get('email')
        name = idinfo.get('name', '')
        picture = idinfo.get('picture', '')
        print("📧 Google Email from token:", email)

        if not email:
            return JsonResponse({'error': 'Email not found in token'}, status=400)

        base_username = email.split('@')[0]
        username = base_username
        i = 1
        while CustomUser.objects.filter(username=username).exists():
            username = f"{base_username}{i}"
            i += 1

        user, created = CustomUser.objects.get_or_create(
            email=email,
            defaults={
                'username': username,
                'full_name': name,
                'password': '',  # Optional: not used in Google login
            }
        )

        login(request, user)
        refresh = RefreshToken.for_user(user)

        return JsonResponse({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'new_user': created,
            'email': user.email,
            'username': user.username,
        })

    except Exception as e:
        import traceback
        traceback.print_exc()
        return JsonResponse({'error': str(e)}, status=500)


# -------------------- Logout --------------------

def logout_view(request):
    logout(request)
    return JsonResponse({'status': 'logged out'})

# -------------------- Dashboard Data --------------------

@login_required
def dashboard_data_view(request):
    alerts = Alert.objects.filter(user=request.user)
    stocks = Stock.objects.all()

    return JsonResponse({
        'alerts': [
            {
                'stock': alert.stock.symbol,
                'target_price': alert.target_price,
                'condition': alert.condition,
                'latest_price': alert.stock.latest_price,
                'status': 'Triggered' if alert.is_triggered else 'Active'
            }
            for alert in alerts
        ],
        'stocks': [
            {
                'symbol': stock.symbol,
                'company_name': stock.company_name,
                'latest_price': stock.latest_price
            }
            for stock in stocks
        ],
        'user': {
            'full_name': request.user.full_name,
            'username': request.user.username,
            'email': request.user.email,
        },
    })

# -------------------- Password Reset Flow --------------------

def forgot_password_view(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = CustomUser.objects.get(email=email)

            otp = generate_otp()
            PasswordResetOTP.objects.create(user=user, otp=otp)

            send_mail(
                subject='Your Password Reset OTP',
                message=f'Your OTP for password reset is: {otp}',
                from_email=os.getenv("OTP_FROM_EMAIL"),
                recipient_list=[email],
                fail_silently=False,
            )

            request.session['reset_email'] = email
            request.session.modified = True

            return JsonResponse({'status': 'otp_sent'})
        return JsonResponse({'errors': form.errors}, status=400)
    return JsonResponse({'error': 'GET not allowed'}, status=405)

def verify_otp_view(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        email = request.session.get('reset_email')

        if not email:
            return JsonResponse({'error': 'Session expired'}, status=400)

        user = CustomUser.objects.filter(email=email).first()
        otp_record = PasswordResetOTP.objects.filter(user=user, otp=entered_otp).first()

        if otp_record:
            otp_record.delete()
            return JsonResponse({'status': 'verified'})
        else:
            return JsonResponse({'error': 'Invalid OTP'}, status=400)

    return JsonResponse({'error': 'GET not allowed'}, status=405)

def reset_password_view(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        email = request.session.get('reset_email')

        if not email:
            return JsonResponse({'error': 'Session expired'}, status=400)

        if password != confirm_password:
            return JsonResponse({'error': 'Passwords do not match'}, status=400)

        user = CustomUser.objects.filter(email=email).first()
        if user:
            user.password = make_password(password)
            user.save()
            del request.session['reset_email']
            request.session.modified = True
            return JsonResponse({'status': 'password_reset'})
    return JsonResponse({'error': 'GET not allowed'}, status=405)

# -------------------- User Info --------------------

@login_required
def user_profile_view(request):
    return JsonResponse({
        "full_name": request.user.full_name,
        "username": request.user.username,
        "email": request.user.email
    })

# -------------------- Alert Checker --------------------

@login_required
def check_alert_notifications(request):
    triggered_alerts = Alert.objects.filter(user=request.user, is_triggered=True).order_by('-triggered_at')
    return JsonResponse({
        'alerts': [
            {
                'stock': alert.stock.symbol,
                'message': f"{alert.stock.symbol} hit target price {alert.target_price} ({alert.condition})"
            }
            for alert in triggered_alerts
        ]
    })

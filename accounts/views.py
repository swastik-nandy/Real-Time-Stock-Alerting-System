from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import CustomUserCreationForm, CustomAuthenticationForm, ForgotPasswordForm
from alerts.forms import AlertForm
from django.contrib import messages
from .models import CustomUser, PasswordResetOTP
from .utils import generate_otp
from django.core.mail import send_mail
from django.conf import settings
from alerts.models import Alert
from stocks.models import Stock
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from alerts.models import Alert
from django.utils.timezone import now
import os
import json
from django.views.decorators.csrf import csrf_exempt
from .models import PushSubscription
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect


# -------------------- Account Views --------------------

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect


# -------------------- Login Views --------------------

from django.contrib.auth import login
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import CustomAuthenticationForm

def login_view(request):
    form = CustomAuthenticationForm(request, data=request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            user = form.get_user()
            if user.is_superuser or user.is_staff:
                messages.error(request, "Admin users cannot login from here.")
                return redirect('login')
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid email or password.")

    return render(request, 'accounts/login.html', {'form': form})


# -------------------- Dashboard Views --------------------

def dashboard_view(request):
    if request.method == 'POST':
        form = AlertForm(request.POST)
        if form.is_valid():
            alert = form.save(commit=False)
            alert.user = request.user
            alert.save()
            messages.success(request, "Alert created successfully!")
            return redirect('dashboard')
    else:
        form = AlertForm()

    user_alerts = Alert.objects.filter(user=request.user)
    stocks = Stock.objects.all()

    context = {
        'form': form,
        'user_alerts': user_alerts,
        'stocks': stocks,
        'full_name': request.user.full_name,
        'username': request.user.username,
        'email': request.user.email,
        'trending_stocks': stocks,  # sending trending stocks too
        'vapid_public_key': settings.VAPID_PUBLIC_KEY,

    }
    return render(request, 'accounts/dashboard.html', context)

def refresh_trending_stocks_view(request):
    stocks = Stock.objects.all()
    html = render_to_string('accounts/partials/trending_stocks_table.html', {'trending_stocks': stocks})
    return JsonResponse({'html': html})

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

            messages.success(request, 'OTP has been sent to your email. Please check your inbox.')
            return redirect('verify_otp')
    else:
        form = ForgotPasswordForm()

    return render(request, 'accounts/forgot_password.html', {'form': form})

def verify_otp_view(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        email = request.session.get('reset_email')

        if not email:
            messages.error(request, 'Session expired. Please try again.')
            return redirect('forgot_password')

        user = CustomUser.objects.filter(email=email).first()
        otp_record = PasswordResetOTP.objects.filter(user=user, otp=entered_otp).first()

        if otp_record:
            otp_record.delete()
            return redirect('reset_password')
        else:
            messages.error(request, 'Invalid OTP. Please try again.')
            return redirect('verify_otp')

    return render(request, 'accounts/verify_otp.html')

def reset_password_view(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        email = request.session.get('reset_email')

        if not email:
            messages.error(request, 'Session expired. Please start again.')
            return redirect('forgot_password')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('reset_password')

        user = CustomUser.objects.filter(email=email).first()
        if user:
            user.password = make_password(password)
            user.save()

            del request.session['reset_email']
            request.session.modified = True

            messages.success(request, 'Password reset successfully. Please login.')
            return redirect('login')

    return render(request, 'accounts/reset_password.html')




def check_alert_notifications(request):
    if not request.user.is_authenticated:
        return JsonResponse({'alerts': []})

    triggered_alerts = Alert.objects.filter(user=request.user, is_triggered=True).order_by('-triggered_at')

    data = []
    for alert in triggered_alerts:
        data.append({
            'stock': alert.stock.symbol,
            'message': f"{alert.stock.symbol} has reached your target price of {alert.target_price} ({alert.condition})!",
        })

    return JsonResponse({'alerts': data})


@csrf_exempt
def save_subscription_view(request):
    if request.method == 'POST' and request.user.is_authenticated:
        data = json.loads(request.body)
        PushSubscription.objects.update_or_create(
            user=request.user,
            defaults={
                'endpoint': data['endpoint'],
                'auth': data['keys']['auth'],
                'p256dh': data['keys']['p256dh']
            }
        )
        return JsonResponse({'status': 'subscription saved'})
    return JsonResponse({'error': 'Unauthorized or invalid'}, status=400)


from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    return redirect('login')  


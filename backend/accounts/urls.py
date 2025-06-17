from django.urls import path
from . import views

urlpatterns = [
    # Auth endpoints
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Google OAuth via React
    path('auth/google-login/', views.google_login_view, name='google_login'),

    # Logged-in user info
    path('user/', views.user_profile_view, name='user_info'),

    # Dashboard data for UI
    path('dashboard/', views.dashboard_data_view, name='dashboard_data'),

    # Password + OTP flows
    path('forgot-password/', views.forgot_password_view, name='forgot_password'),
    path('verify-otp/', views.verify_otp_view, name='verify_otp'),
    path('reset-password/', views.reset_password_view, name='reset_password'),

    # Push alert notifications (triggered alert summaries)
    path('check-alerts/', views.check_alert_notifications, name='check_alerts'),
]

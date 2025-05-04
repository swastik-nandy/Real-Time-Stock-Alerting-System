from django.urls import path
from . import views
from .views import check_alert_notifications
from .views import save_subscription_view


urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('forgot-password/', views.forgot_password_view, name='forgot_password'),
    path('verify-otp/', views.verify_otp_view, name='verify_otp'),
    path('reset-password/', views.reset_password_view, name='reset_password'),

    # New endpoint for refreshing trending stocks dynamically
    path('refresh-trending-stocks/', views.refresh_trending_stocks_view, name='refresh_trending_stocks'),
    path('check-alerts/', check_alert_notifications, name='check_alerts'),
    path('save-subscription/', save_subscription_view, name='save_subscription'),




    
]
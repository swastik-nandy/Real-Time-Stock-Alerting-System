from django.urls import path
from .views import NotificationListAPIView

urlpatterns = [
    path('', NotificationListAPIView.as_view(), name='notification-list'),
]

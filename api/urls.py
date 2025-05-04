from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # JWT Authentication routes
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # App-specific API routes
    path('stocks/', include('stocks.urls')),
    path('alerts/', include('alerts.urls')),
    path('notifications/', include('notifications.urls')),
]

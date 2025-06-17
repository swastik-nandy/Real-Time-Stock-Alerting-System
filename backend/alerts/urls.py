from django.urls import path
from .views import AlertListCreateAPIView

urlpatterns = [
    path('alerts/', AlertListCreateAPIView.as_view(), name='alert-list-create'),
]

from django.urls import path
from .views import StockListAPIView, StockDetailAPIView

urlpatterns = [
    path('', StockListAPIView.as_view(), name='stock-list'),
    path('<int:id>/', StockDetailAPIView.as_view(), name='stock-detail'),
]

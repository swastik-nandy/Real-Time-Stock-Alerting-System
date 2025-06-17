from django.urls import path
from .views import StockListAPIView, StockDetailAPIView, trending_stocks_view

urlpatterns = [
    path('', StockListAPIView.as_view(), name='stock-list'),
    path('<int:id>/', StockDetailAPIView.as_view(), name='stock-detail'),
    path('trending/', trending_stocks_view, name='trending-stocks'),
]

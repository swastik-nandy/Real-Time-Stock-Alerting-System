from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Stock
from .serializers import StockSerializer

# GET /api/stocks/
class StockListAPIView(generics.ListAPIView):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer

# GET /api/stocks/<id>/
class StockDetailAPIView(generics.RetrieveAPIView):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    lookup_field = 'id'

# ✅ GET /api/stocks/trending/
@api_view(['GET'])
def trending_stocks_view(request):
    trending = Stock.objects.order_by('-last_updated')[:5]  # you can tweak logic
    serializer = StockSerializer(trending, many=True)
    return Response(serializer.data)

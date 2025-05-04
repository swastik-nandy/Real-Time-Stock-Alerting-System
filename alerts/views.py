from rest_framework.permissions import IsAuthenticated

from rest_framework import generics
from .models import Alert
from .serializers import AlertSerializer

class AlertListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated] 
    queryset = Alert.objects.all()
    serializer_class = AlertSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

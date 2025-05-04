from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from .models import Notification
from .serializers import NotificationSerializer

class NotificationListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    serializer_class = NotificationSerializer

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)

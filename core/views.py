from django.shortcuts import render
from .serializers import EventSerializer
from .models import Event
from rest_framework import generics
from rest_framework.permissions import AllowAny
from .service import publish_event

# Create your views here.

class EventCreateView(generics.CreateAPIView):
    """
    A viewset for viewing and receiving event instances.
    """

    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = self.request.user
        if user.is_authenticated:
            event = serializer.save(actor= user)
        else:
            event = serializer.save()
        
        publish_event(event)

from rest_framework import serializers
from .models import Event




class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event 
        fields = ['actor', 'source', 'event_type','object_type', 'object_id', 'metadata', 'created_at']
        read_only_fields = ['created_at']
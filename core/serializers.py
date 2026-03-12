from rest_framework import serializers
from .models import Event




class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event 
        fields = ['actor', 'source','event_type','object_type', 'object_id', 'metadata', 'created_at']
        read_only_fields = ['created_at', 'actor']

    def validate(self, data):
        actor = data.get('actor')
        source = data.get('source')

        if not actor and not source:
            raise serializers.ValidationError('No user or source ingested')
    
        return data
from rest_framework import serializers
from .models import Event




class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event 
        fields = ['id', 'actor', 'source','event_type','object_type', 'object_id', 'metadata', 'created_at']
        read_only_fields = ['created_at', 'actor']

    def validate(self, data):
        source = data.get('source')

        request = self.context.get('request')
        actor = request.user if request and request.user.is_authenticated else None

        if not actor and not source:
            raise serializers.ValidationError('No user or source ingested')
    
        return data
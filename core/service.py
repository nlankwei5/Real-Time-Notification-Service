from .serializers import EventSerializer
from .models import Event




def publish_event(event):
    """
    this is a service function supposed to get an event object, serialize it to json and publish to kafka
    """

    serializer = EventSerializer(event)
    data = serializer.data

    return data 

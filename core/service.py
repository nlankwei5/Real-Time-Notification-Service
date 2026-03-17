from .serializers import EventSerializer
from .models import Event
import asyncio
from .kafka.producer import send_one




def publish_event(event):
    """
    this is a service function supposed to get an event object, serialize it to json and publish to kafka
    """

    serializer = EventSerializer(event)
    data = serializer.data
    asyncio.run(send_one(data))





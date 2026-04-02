import asyncio
from aiokafka import AIOKafkaConsumer
from django.conf import settings
import json 
from asgiref.sync import sync_to_async
from core.models import  Event, Notification, NotificationPreference
from channels.layers import get_channel_layer

channel_layer = get_channel_layer()


async def consume_messages():
    consumer = AIOKafkaConsumer(
        *settings.KAFKA_TOPICS,
        bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
        group_id=settings.KAFKA_CONSUMER_GROUP,
    )
    await consumer.start()
    try:
        async for msg in consumer:
            data = json.loads(msg.value.decode('utf-8'))
            
            print("consumed: ", data)
            event_type = data['event_type']
            
            result = await sync_to_async(lambda: list(NotificationPreference.objects.filter(
                enabled=True, 
                event_type=event_type
            ).values_list('user', flat=True)))()
            
            print("users to notify: ", result)
            
            event = await sync_to_async(lambda: Event.objects.get(id=data['id']))()
            
            for user in result:
                notification = await sync_to_async(lambda u=user: Notification.objects.create(
                    user_id= u, 
                    event = event,
                ))()

                print(f"Sending to group user_{user}: {notification.id}")

                notification_data = {
                        "id": notification.id,
                        "user_id": notification.user_id,
                        "event_id": event.id,
                        "event_type": event.event_type,
                }
                await channel_layer.group_send(
                    f"user_{user}",  
                    {
                        "type": "send_notification", 
                        "data": notification_data, 
                    }
                )
            
    finally:
        await consumer.stop()



import asyncio
from aiokafka import AIOKafkaConsumer
from django.conf import settings
import json 
from asgiref.sync import sync_to_async
from core.models import  Event, Notification, NotificationPreference



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
    finally:
        await consumer.stop()



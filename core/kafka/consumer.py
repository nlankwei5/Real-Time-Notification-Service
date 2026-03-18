import asyncio
from aiokafka import AIOKafkaConsumer
from django.conf import settings
import json 



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
    finally:
        await consumer.stop()



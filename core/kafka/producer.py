import asyncio
from aiokafka import AIOKafkaProducer
from django.conf import settings
import json


async def send_one(data):
    producer = AIOKafkaProducer(
        bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,)
    
    await producer.start()
    try:
        json_data = json.dumps(data).encode("utf-8")
        # Produce message

        await producer.send_and_wait("events", value= json_data)
        print("Message sent")
    finally:
        # Wait for all pending messages to be delivered or expire.
        await producer.stop()


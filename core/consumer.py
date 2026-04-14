import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from django_redis import get_redis_connection



class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = None
        self.user_id = None

        user = self.scope["user"]

        if user.is_authenticated:
            self.user_id = user.id
            self.group_name = f"user_{user.id}"
        else:
            self.group_name = "notifications"

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

        # Only track in Redis if user is authenticated
        if self.user_id:
            redis = await sync_to_async(get_redis_connection)("default")
            redis.sadd("online_users", self.user_id)
            redis.set(f"last_seen:{self.user_id}", 1, ex=300)

        print(f"Client connected: {self.channel_name} group: {self.group_name}")


    async def disconnect(self, close_code):
        if self.group_name:
            await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name
            )

        # Only clean Redis if user was authenticated
        if self.user_id:
            redis = await sync_to_async(get_redis_connection)("default")
            await sync_to_async(redis.srem)("online_users", self.user_id)

        print(f"Client disconnected: {close_code}")


    async def send_notification(self, event):
        print("send_notification called with:", event)
        await self.send(text_data=json.dumps(event["data"]))
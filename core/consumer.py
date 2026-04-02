import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from django_redis import get_redis_connection



class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope["user"]
        
        if not user.is_authenticated:
            await self.close()
            return
        
        user_id = user.id
        self.user_id = user_id
        self.group_name = f"user_{user_id}"

        await self.channel_layer.group_add(self.group_name, self.channel_name)

        await self.accept()
        
        redis = await sync_to_async(get_redis_connection)("default")
        redis.sadd("online_users", self.user_id)
        redis.set(f"last_seen:{self.user_id}", 1, ex=300)

    

    async def disconnect(self, close_code):
        if self.group_name:  
            await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name
            )
            redis = await sync_to_async(get_redis_connection)("default")
            await sync_to_async(redis.srem)("online_users", self.user_id)
        
        print(f"Client disconnected: {close_code}")

    async def send_notification(self, event):
        print("send_notification called with:", event)
        
        await self.send(text_data=json.dumps(event["data"]))
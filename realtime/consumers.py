import json
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from asgiref.sync import async_to_sync

class EventConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        with open('log.txt', 'w') as f:
            import sys
            original_stdout = sys.stdout
            sys.stdout = f
            print(self.scope['url_route'])

            sys.stdout = original_stdout
            f.close()
        
        self.room_name = 'admin'
        self.group_name = 'admin'
        await self.channel_layer.group_add(
            self.group_name, self.channel_name
        )

        await self.accept()
    
    async def notification_visit(self, event):
        data = event['message']
        await self.send(text_data=data)
    
    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.group_name, 
            self.channel_name
        )

import json
from channels.generic.websocket import AsyncWebsocketConsumer

class LikeConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        
        await self.send(text_data=json.dumps({
            'type': 'connection_established',
            'message': 'you are now connected! :)'
        }))
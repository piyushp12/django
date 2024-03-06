import json
from channels.generic.websocket import AsyncWebsocketConsumer
from App.models import DivergenceScreener, BrakerScreener
from channels.db import database_sync_to_async
from App.serializers import LoduScreenerSerializer

class DivergenceScreenerConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Connect to the group for DivergenceScreener events
        await self.channel_layer.group_add(
            "divergence",
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Disconnect from the group
        await self.channel_layer.group_discard(
            "divergence",
            self.channel_name
        )

    async def send_divergence_notification(self, event):
        # Send the DivergenceScreener notification to the WebSocket
        await self.send(text_data=json.dumps(event))
        
class BrakerScreenerConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Connect to the group for BrakerScreener events
        await self.channel_layer.group_add(
            "braker",
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Disconnect from the group
        await self.channel_layer.group_discard(
            "braker",
            self.channel_name
        )

    async def send_braker_notification(self, event):
        # Send the BrakerScreener notification to the WebSocket
        await self.send(text_data=json.dumps(event))
        
        


class BrakerScreenerConsumerNew(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add(
            "braker_data",
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            "braker_data",
            self.channel_name
        )

    async def send_braker_notification(self, event):
        await self.send(text_data=json.dumps(event))
        
    async def send_divergence_notification(self, event):
        await self.send(text_data=json.dumps(event))
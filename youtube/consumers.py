
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync,sync_to_async
import json
from .models import *



class SendThumbnails(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['socket_url']
        self.room_group_name = 'socket_url%s' % self.room_name
        print(self.room_group_name)
        
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()
        
        self.send(text_data=json.dumps({
            'payload': 'connected'
        }))

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'order_status',
                'payload': text_data
            }
        )

    # Receive message from room group
    def send_thumbnails(self, event):
        print(event)
        data = json.loads(event['value'])
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'payload': data
        }))
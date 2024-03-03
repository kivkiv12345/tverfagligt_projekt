import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


# Class has been partly revised by ChatGPT
class ServerConsumer(WebsocketConsumer):

    def connect(self):
        self.server_id = self.scope["url_route"]["kwargs"]["server_id"]
        self.room_group_name = f"server_{self.server_id}"

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "chat.message", "message": message}
        )

    # Receive message from room group
    def server_event(self, event):
        # Handle server-specific events
        message = event["message"]
        self.send(text_data=json.dumps({"message": message}))

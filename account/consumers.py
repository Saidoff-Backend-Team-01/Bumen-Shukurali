import base64
import json
import secrets
from datetime import datetime

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.core.files.base import ContentFile

from account.models import User, UserGroupConversation, UserMessage



class ChatConsumer(WebsocketConsumer):
    def connect(self):
        # print("here")
        # self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
     
        self.room_group_name = f"chat_first_room_group"

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
        # parse the json data into dictionary object
        text_data_json = json.loads(text_data)
        print("text data: ", text_data_json)
        # Send message to room group
        chat_type = {"type": "chat_message"}
        return_dict = {**chat_type, **text_data_json}
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            return_dict,
        )


    def chat_message(self, event):
        text_data_json = event.copy()
        text_data_json.pop("type")
        message, attachment = (
            text_data_json["message"],
            text_data_json.get("attachment"),
        )
        print("MEssage for chat message m", message)

        conversation = UserGroupConversation.objects.get_or_create(id=int(1))
        sender = self.scope['user']

        # Attachment
        if attachment:
            file_str, file_ext = attachment["data"], attachment["format"]

            file_data = ContentFile(
                base64.b64decode(file_str), name=f"{secrets.token_hex(8)}.{file_ext}"
            )
            _message = UserMessage.objects.create(
                sender=sender,
                attachment=file_data,
                text=message,
                conversation_id=conversation,
            )
        else:
            _message = UserMessage.objects.create(
                sender=sender,
                text=message,
                conversation_id=conversation,
            )
 
        # Send message to WebSocket
        self.send(
            text_data={
                "message": _message
            }
        )

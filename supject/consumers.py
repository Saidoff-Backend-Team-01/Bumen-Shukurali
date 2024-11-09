import json

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from account.models import Groups, User, UserMessage
from common.models import Media
from supject.utils import download_image
from supject.models import Club, UserClubMessage
from core.settings import HOST


class GeneralChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if self.scope['user'].is_anonymous:
            return 

        self.room_name = 'general_chat'
        self.room_group_name = f'chat_{self.room_name}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        messages = await self.get_messages()
        await self.send(text_data=json.dumps({
            'messages': messages
        }))

    
    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    
    async def receive(self, text_data):
        json_text_data = json.loads(text_data)
        user = self.scope['user']
        action = json_text_data.get('action', 'send')
        

        if action == 'send':
            file = json_text_data.get('file', None)


            message = json_text_data['message']
            msg = await self.create_message(msg=message, user=user, file=file)  


            await self.channel_layer.group_send(
                self.room_group_name,
                {   
                    'type': 'chat_message',
                    'action': 'send',
                    'id': msg['id'],
                    'message': msg['message'],
                    'user': msg['user'],
                    'file': msg['file']
                }
            )  


        elif action == 'delete':
            message_id = json_text_data.get('message_id')

            await self.delete_message(user=user, message_id=message_id)

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'action': 'delete',
                    'message_id': message_id,
                    'Is_deleted': 'Message was successfuly deleted !!!'
                }
            )
        

        elif action == 'edit':
            new_message = json_text_data['new_message']
            message_id = json_text_data.get('message_id')
            file = json_text_data.get('file', None)
            old_message = await self.edit_message(user=user, message_id=message_id, new_message=new_message)

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'action': 'edit',
                    'id': old_message.get('id'),
                    'new_message': old_message.get('new_message'),
                    'user': old_message.get('user'),
                    'file': old_message.get('file'),
                }
            )  


    async def chat_message(self, event):
        action = event['action']


   
        if action == 'send':
            id = event['id']
            message = event.get('message')
            user = event.get('user')
            file = event.get('file')

            await self.send(
                text_data=json.dumps({
                    'id': id,
                    'message': message,
                    'user': user,
                    'file': file
                })
            )  

        elif action == 'delete':
            message_id = event.get('message_id')
            is_deleted = event.get('Is_deleted')

            await self.send(
                text_data=json.dumps({
                    'message_id': message_id,
                    'is_deleted': is_deleted,
                })
            )  

        elif action == 'edit':
            id = event['id']
            new_message = event.get('new_message')
            user = event.get('user')
            file = event.get('file')

            await self.send(
                text_data=json.dumps({
                    'id': id,
                    'new_message': new_message,
                    'user': user,
                    'file': file
                })
            )  


    @database_sync_to_async
    def get_messages(self):
        msg = UserMessage.objects.all()
        return [
             { 
                'id': i.pk,  
                'message': i.message, 
                'user': {
                        'id': i.user.pk, 
                        'username': i.user.username, 
                        'photo': f'{HOST}/media/{i.user.photo.file}/' if i.user.photo else None 
                }, 
                'file': f'{HOST}/media/{i.file.file}/' if bool(i.file) else None,
                'created_at': str(i.created_at) 
             } 
             for i in msg
            ]

    
    @database_sync_to_async
    def create_message(self, msg, user, file=None):
        group = Groups.objects.first()
    
        if group is None:
            raise ValueError("Группа не найдена, сообщение не может быть создано.")

        msg = UserMessage.objects.create(message=msg, user=user, group=group)

        if file:
            print('File: ', file, 'Message: ', msg)
            media = Media.objects.create(file=download_image(img_url=file, message_id=msg.pk), type='file')
            msg.file = media
            msg.save()
        

        return {   
                    'id': msg.pk,
                    'message': msg.message,
                    'user': {'id': msg.user.pk, 'username': msg.user.username, 'photo': f'{HOST}/media/{msg.user.photo.file}/' if msg.user.photo else None },
                    'file': f'{HOST}/media/{msg.file.file}/' if bool(msg.file) else None
                }
    
    @database_sync_to_async
    def delete_message(slef, user, message_id):
        try:
            UserMessage.objects.get(pk=message_id, user=user).delete()

        except:
            raise ValueError('User or message was not found !!!')
    

    @database_sync_to_async
    def edit_message(self, user, message_id, new_message):
        try:
            old_message = UserMessage.objects.get(pk=int(message_id), user=user)
            old_message.message = new_message
            old_message.save()

            return {   
                    'id': old_message.pk,
                    'new_message': old_message.message,
                    'user': {'id': old_message.user.pk, 'username': old_message.user.username, 'photo': f'{HOST}/media/{old_message.user.photo.file}/' if old_message.user.photo else None },
                    'file': f'{HOST}/media/{old_message.file.file}/' if bool(old_message.file) else None
                }

        except:
            raise ValueError('User or message was not found !!!')



class SujectChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_club_{self.room_name}'


        if self.scope['user'].is_anonymous:
            return 
        
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
        )

        await self.accept()

        messages = await self.send_messages(self.room_name)
        await self.send(text_data=json.dumps({
            'messages': messages
        }))


    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name,
        )
    

    async def receive(self, text_data):
        json_text_data = json.loads(text_data)
        user = self.scope['user']
        action = json_text_data.get('action', 'send')
        

        if action == 'send':
            file = json_text_data.get('file', None)


            message = json_text_data['message']
            msg = await self.create_message(msg=message, user=user, file=file, room_name=self.room_name)  


            await self.channel_layer.group_send(
                self.room_group_name,
                {   
                    'type': 'chat_message',
                    'action': 'send',
                    'id': msg['id'],
                    'message': msg['message'],
                    'user': msg['user'],
                    'file': msg['file']
                }
            )  


        elif action == 'delete':
            message_id = json_text_data.get('message_id')

            await self.delete_message(user=user, message_id=message_id)

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'action': 'delete',
                    'message_id': message_id,
                    'Is_deleted': 'Message was successfuly deleted !!!'
                }
            )
        

        elif action == 'edit':
            new_message = json_text_data['new_message']
            message_id = json_text_data.get('message_id')
            file = json_text_data.get('file', None)
            old_message = await self.edit_message(user=user, message_id=message_id, new_message=new_message)

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'action': 'edit',
                    'id': old_message.get('id'),
                    'new_message': old_message.get('new_message'),
                    'user': old_message.get('user'),
                    'file': old_message.get('file'),
                }
            )  

        
    

    async def chat_message(self, event):
        print('fervwqvsfa', event)
        action = event['action']

        
   
        if action == 'send':
            id = event['id']
            message = event.get('message')
            user = event.get('user')
            file = event.get('file')

            await self.send(
                text_data=json.dumps({
                    'id': id,
                    'message': message,
                    'user': user,
                    'file': file,
                    'room': self.room_name,
                })
            )  

        elif action == 'delete':
            message_id = event.get('message_id')
            is_deleted = event.get('Is_deleted')

            await self.send(
                text_data=json.dumps({
                    'message_id': message_id,
                    'is_deleted': is_deleted,
                })
            )  

        elif action == 'edit':
            id = event['id']
            new_message = event.get('new_message')
            user = event.get('user')
            file = event.get('file')

            await self.send(
                text_data=json.dumps({
                    'id': id,
                    'new_message': new_message,
                    'user': user,
                    'file': file
                })
            )  

    
    @database_sync_to_async
    def send_messages(self, room_name):
        try:
            club = Club.objects.get(name=room_name)
        except:
            raise ValueError('404! Club was not found')
        messages = UserClubMessage.objects.all().filter(club=club)

        if not messages:
            return []


        return [
             {
              'id': msg.pk, 
              'msg': msg.message, 
              'file': f'{HOST}/media/{msg.file.file}/' if bool(msg.file) else None, 
              'user': {'id': msg.user.pk, 
                       'username': msg.user.username, 
                       'photo': f'{HOST}/media/{msg.user.photo.file}/' if bool(msg.user.photo) else None },
              'created_at': str(msg.created_at)
                       }
              
              for msg in messages
            ]
    

    @database_sync_to_async
    def create_message(self, msg, user, room_name, file=None):
        try:
            club = Club.objects.get(name=room_name)
        except:
            raise ValueError('404! Club was not found')
    

        msg = UserClubMessage.objects.create(message=msg, user=user, club=club)

        if file:
            media = Media.objects.create(file=download_image(img_url=file, message_id=msg.pk), type='file')
            msg.file = media
            msg.save()
        
        return {   
                    'id': msg.pk,
                    'message': msg.message,
                    'user': {'id': msg.user.pk, 'username': msg.user.username, 'photo': f'{HOST}/media/{msg.user.photo.file}/' if msg.user.photo else None },
                    'file': f'{HOST}/media/{msg.file.file}/' if bool(msg.file) else None
                }
    

    @database_sync_to_async
    def delete_message(slef, user, message_id):
        try:
            UserClubMessage.objects.get(pk=message_id, user=user).delete()

        except:
            raise ValueError('User or message was not found !!!')
    

    @database_sync_to_async
    def edit_message(self, user, message_id, new_message):
        try:
            old_message = UserClubMessage.objects.get(pk=int(message_id), user=user)
            old_message.message = new_message
            old_message.save()

            return {   
                    'id': old_message.pk,
                    'new_message': old_message.message,
                    'user': {'id': old_message.user.pk, 'username': old_message.user.username, 'photo': f'{HOST}/media/{old_message.user.photo.file}/' if old_message.user.photo else None },
                    'file': f'{HOST}/media/{old_message.file.file}/' if bool(old_message.file) else None
                }

        except:
            raise ValueError('User or message was not found !!!')

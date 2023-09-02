from channels.generic.websocket import AsyncWebsocketConsumer
from live_interaction.models import Room
from Users.models import CustomUser
import json
from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async


class Live_Music_Consumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("connection esblished")
        self.user = self.scope['user']
        user = self.scope['user']

        print(type(self.user.username))
        self.RoomName = self.scope['url_route']['kwargs']['groupName'].replace(
            '"', "")
        self.room = await database_sync_to_async(Room.objects.get)(name=self.RoomName)
        user_present = await database_sync_to_async(self.room.users.filter(id=self.user.id).exists)()
        if not user_present:
            await database_sync_to_async(self.room.users.add)(self.user)
            self.room.user_num += 1
            await database_sync_to_async(self.room.save)()
            print("user added")
        try:
            admin = await sync_to_async(lambda: self.room.admin)()
            print(admin)
            self.admin = admin
        except Exception as e:
            print(str(e))
        await database_sync_to_async(lambda: self.room.users.add(user))()
        await self.channel_layer.group_add(
            self.RoomName,
            self.channel_name
        )
        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        username = data['username'].replace('"', '')
        if self.user == self.admin:
            print("Data received from the user :", text_data)
            print(data)
            print(type(data['message']))
            if isinstance(data['message'], float):
                self.room.timeFix = data['message']
                await database_sync_to_async(self.room.save)()
                print("time updated")
            elif isinstance(data['message'], bool):
                self.room.state = data['message']
                await database_sync_to_async(self.room.save)()
                print("state updated")
            # else:
            #     if isinstance(data['message'], str):
            #         await self.channel_layer.group_send(
            #             self.RoomName,
            #             {
            #                 'type': 'chat.message',
            #                 'message': data['message'],
            #                 'username':data['username']
            #             }
            #         )
        if not isinstance(data['message'], float):
            await self.channel_layer.group_send(
                self.RoomName,
                {
                    "type": "chat.message",
                    'message': data['message'],
                    'username': username
                }
            )

    async def chat_message(self, event):
        print("message sendx")
        message = event['message']
        username = event['username']
        print("username :", username)
        await self.send(json.dumps({'message': message, 'username': username}))

    async def disconnect(self, close_code):
        print("connection disclosed", close_code)
        if self.admin == self.user:
            await self.channel_layer.group_send(
                self.RoomName,
                {
                    'type': 'group.disable',
                    'message': 'disabled'
                }
            )

            # await database_sync_to_async(self.room.delete)()
            print("group deleted")
        else:
            self.room.user_num -= 1
            await database_sync_to_async(self.room.users.remove)(self.user)
            await database_sync_to_async(self.room.save)()
            print("normal user leaved")
            print(f"{self.user.username} leaves ")
        await self.channel_layer.group_discard(
            self.RoomName,
            self.channel_name
        )

    async def group_disable(self, event):
        message = event['message']
        await self.send(json.dumps({'message': message}))

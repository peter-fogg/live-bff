from channels.auth import get_user, login
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

import json

class ChatApiConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        user = await get_user(self.scope)
        if user.is_anonymous:
            await self.close()
        else:
            # TODO: later it should be ensured that the user belongs
            # to this chat session but for now just let them use the
            # url they get
            await self.channel_layer.group_add(self.chat_id, self.channel_name)
            await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.chat_id, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)

        await self.channel_layer.group_send(
            self.chat_id,
            {'type': 'chat_message', 'message': text_data_json['message']}
        )

    async def chat_message(self, event):
        await self.send(json.dumps({'message': event['message']}))

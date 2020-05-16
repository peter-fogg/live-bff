from channels.auth import AuthMiddlewareStack
from channels.db import database_sync_to_async
from channels.routing import URLRouter
from channels.testing import WebsocketCommunicator
from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse, re_path

import datetime
import json
import pytest

from livebff.chat_api.consumers import ChatApiConsumer
from livebff.chat_api.routing import websocket_urlpatterns

@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_chat_socket():
    client = Client()
    user = await database_sync_to_async(create_test_user)()
    await database_sync_to_async(client.force_login)(user=user)
    application = AuthMiddlewareStack(URLRouter(websocket_urlpatterns))
    communicator = WebsocketCommunicator(
        application,
        'ws/chat_api/0123456789/',
        headers = [(
            b'cookie',
            f'sessionid={client.cookies["sessionid"].value}'.encode('ascii')
        )]
    )
    connected, _ = await communicator.connect()
    assert connected
    json_data = {'message': 'hello world'}
    await communicator.send_to(text_data=json.dumps(json_data))
    response = await communicator.receive_from()
    assert json.loads(response) == json_data
    await communicator.disconnect()

def create_test_user(
        username='tnorgay',
        password='snow',
        birth_date=datetime.date(1953, 5, 29)
):
    user = User.objects.create(username=username, password=password)
    user.refresh_from_db()
    user.profile.birth_date = birth_date
    user.save()
    return user

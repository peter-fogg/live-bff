from channels.testing import WebsocketCommunicator
from django.urls import reverse
import pytest

from livebff.chat_api.consumers import ChatApiConsumer

@pytest.mark.asyncio
async def test_chat_socket():
    communicator = WebsocketCommunicator(ChatApiConsumer, reverse('ws_chat'))
    connected, _ = await communicator.connect()
    assert connected
    text = 'hello world'
    await communicator.send_to(text_data=text)
    response = communicator.receive_from()
    assert response == text
    await communicator.disconnect()

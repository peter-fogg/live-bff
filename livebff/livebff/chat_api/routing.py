from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat_api/(?P<chat_id>[0-9]{10})/$', consumers.ChatApiConsumer)
]

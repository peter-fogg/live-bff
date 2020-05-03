from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

from livebff.chat_api import routing

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(URLRouter(routing.websocket_urlpatterns))
})

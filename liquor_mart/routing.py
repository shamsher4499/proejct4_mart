from django.urls import path, re_path
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from chat_support.consumer import ChatConsumer
# from app.consumers import WebChatConsumer, WebGroupChatConsumer

application = ProtocolTypeRouter({
    "websocket": AuthMiddlewareStack(
        URLRouter([
            re_path('ws/chat/(?P<room_name>\w+)/$', ChatConsumer.as_asgi()),
        ]),
    ),
})
# your_app_name/routing.py

from routing import ProtocolTypeRouter, URLRouter
from auth import AuthMiddlewareStack
from django.urls import re_path
from . import consumer

websocket_urlpatterns= [
    re_path(r'',consumer.ChatConsumer.as_agi),
]


application = ProtocolTypeRouter({
    "websocket": AuthMiddlewareStack(
        URLRouter(
            [
                # Add the path for your WebSocket consumer
                path("ws/video_chat/", VideoChatConsumer.as_asgi()),
            ]
        )
    ),
})
application = ProtocolTypeRouter({
    "websocket": AuthMiddlewareStack(
        URLRouter(
            # Add your WebSocket consumers here
        )
    ),
})

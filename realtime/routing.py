from .import consumers
from django.urls import path

websocket_urlpatterns = [
    path('ws/event/', consumers.EventConsumer.as_asgi())
]

from django.urls import path
from .import consumers
websocket_urls = [
    path('ws/live_music/<str:groupName>/',
         consumers.Live_Music_Consumer.as_asgi(), name="live_music")
]

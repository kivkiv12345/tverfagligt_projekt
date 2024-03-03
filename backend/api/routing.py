from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/server/(?P<server_id>\d+)/$", consumers.ServerConsumer.as_asgi()),
]

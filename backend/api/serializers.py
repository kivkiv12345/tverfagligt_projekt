from rest_framework import serializers
from .models import GameServer


# Source: https://chat.openai.com
class GameServerSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameServer
        fields = ['id', 'server_name', 'default_permissions', 'game', 'server_version', 'is_running', 'ports_used']

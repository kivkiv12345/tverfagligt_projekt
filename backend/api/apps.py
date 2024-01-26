from django.apps import AppConfig
from .docker_compose_manager import AbstractDockerComposeGameServerManager

class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

class VintageStoryManager(AbstractDockerComposeGameServerManager):
    compose_file = 'docker-compose/vintage-story_server/docker-compose.yml'

    game_versions = (
        '1.19.2',
        '1.18.15',
        '1.18.1',
    )

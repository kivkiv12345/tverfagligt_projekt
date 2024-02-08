from django.apps import AppConfig
from api.gameserver_manager.docker_compose_manager import AbstractDockerComposeGameServerManager, \
    GitHubVersionedDockerComposeManager
from api.gameserver_manager.github_versioned_manager import GitHubVersionedManager


class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'


class VintageStoryManager(GitHubVersionedDockerComposeManager):
    #compose_file = 'docker-compose/vintage-story_server/docker-compose.yml'
    compose_file = 'repos/docker-vintagestory/docker-compose.yml'
    version_commit_map = {
        'newest': 'master',
        '1.19.3': '5ce36b8a75e909fa30bfdca9f20a2ac46000fdbf',
        '1.19.2': '71fab0d025eecbd73884be8dedced5c65226298d',
        '1.18.15': 'dd4818b90f74786442f7d1985bcb644915d884c1',
        '1.18.1': '558e4aa364a38f1ea8af1caf32c4f94240bfba1a',
    }
    repo = 'https://github.com/Devidian/docker-vintagestory.git'
    services = ['vsserver-local',]

    game_versions = (
        'newest',
        '1.19.3',
        '1.19.2',
        '1.18.15',
        '1.18.1',
    )

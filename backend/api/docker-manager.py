from abc import ABC

import docker
from docker import DockerClient

from api.gameserver_manager import AbstractGameServerManager


class AbstractDockerImageGameServerManager(AbstractGameServerManager, ABC):
    docker_image: str = None
    client: DockerClient

    def __init__(self, server_name: str):
        self.client = docker.from_env()  # Should instantiate a client per instance, is this what we want?
        super().__init__(server_name)

    def __init_subclass__(cls) -> None:
        assert cls.docker_image is not None,\
            'Subclassed AbstractDockerImageGameServerManager must specify a Docker image'
        super().__init_subclass__()

from abc import ABC
from typing import Iterable

from python_on_whales import DockerClient

from api.gameserver_manager.base_manager import AbstractGameServerManager


class AbstractDockerComposeGameServerManager(AbstractGameServerManager, ABC):
    compose_file: str = None
    client: DockerClient
    services: list[str] | str = None  # services must be a list when multiple, because of python-on-whales reasons

    def __init__(self, server_name: str) -> None:
        # TODO Kevin: Everything will most likely explode if the server_name/compose_project_name is changed.
        # TODO Kevin: Also, how can we make sure the project name prefix is applied to containers when container_name
        #   is specified in the docker-compose.yml file?
        # self.client = DockerClient(compose_files=[self.compose_file], compose_env_file= , compose_project_name=server_name)
        self.client = DockerClient(compose_files=[self.compose_file], compose_project_name=server_name.lower().replace(' ', '_'))
        super().__init__(server_name)

    def __init_subclass__(cls) -> None:
        """ The only purpose of AbstractDockerComposeGameServerManager.__init_subclass__()
            is to ensure that subclasses specify a compose_file """

        super().__init_subclass__()

        # Only non-abstract classes should be registered to the manager dictionary.
        # They may be better ways to check if the subclass is still abstract.
        #   What if the user doesn't know to subclass ABC ?
        #   inspect.isabstract() doesn't appear to work for AbstractDockerComposeGameServer sadly
        if ABC in cls.__bases__:
            return

        assert cls.compose_file is not None,\
            f"Subclassed AbstractDockerComposeGameServerManagers {cls} must specify a docker-compose file"

    def start(self):
        # TODO Kevin: .start() or .up()? I dont know.
        self.client.compose.up(detach=True, services=list(self.services))

    def stop(self):
        # TODO Kevin: .stop() or .down()? I dont know.
        self.client.compose.stop()

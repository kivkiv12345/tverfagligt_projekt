from abc import ABC

from python_on_whales import DockerClient

from api.gameserver_manager import AbstractGameServerManager


class AbstractDockerComposeGameServerManager(AbstractGameServerManager, ABC):
    compose_file: str = None
    client: DockerClient

    def __init__(self, server_name: str) -> None:
        # TODO Kevin: Everything will most likely explode if the server_name/compose_project_name is changed.
        # self.client = DockerClient(compose_files=[self.compose_file], compose_env_file= , compose_project_name=server_name)
        self.client = DockerClient(compose_files=[self.compose_file], compose_project_name=server_name.lower().replace(' ', '_'))
        super().__init__(server_name)

    def __init_subclass__(cls) -> None:
        """ The only purpose of AbstractDockerComposeGameServerManager.__init_subclass__()
            is to ensure that subclasses specify a compose_file """
        assert cls.compose_file is not None,\
            'Subclassed AbstractDockerComposeGameServerManagers must specify a docker-compose file'
        super().__init_subclass__()

    def start(self):
        # TODO Kevin: .start() or .up()? I dont know.
        self.client.compose.up(detach=True)

    def stop(self):
        # TODO Kevin: .stop() or .down()? I dont know.
        self.client.compose.stop()

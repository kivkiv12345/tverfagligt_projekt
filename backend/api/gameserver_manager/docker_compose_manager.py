from __future__ import annotations

from os import path
from os import PathLike

import yaml
from abc import ABC
from typing import Iterable

try:
    from python_on_whales import DockerClient
except (ModuleNotFoundError, ImportError) as e:
    raise ModuleNotFoundError(f"Failed to import python_on_whales, install with 'pip3 install python_on_whales'") from e

from api.gameserver_manager.base_manager import AbstractGameServerManager


COMPOSE_FILES_DIR: PathLike | str = 'compose_files/'


class AbstractDockerComposeGameServerManager(AbstractGameServerManager, ABC):
    compose_file: str = None
    client: DockerClient
    services: list[str] | str = None  # services must be a list when multiple, because of python-on-whales reasons

    def __init__(self, server_name: str) -> None:
        # TODO Kevin: Everything will most likely explode if the server_name/compose_project_name is changed.
        # TODO Kevin: Also, how can we make sure the project name prefix is applied to containers when container_name
        #   is specified in the docker-compose.yml file?
        # self.client = DockerClient(compose_files=[self.compose_file], compose_env_file= , compose_project_name=server_name)
        self.client = DockerClient(compose_files=[self.compose_file],
                                   compose_project_name=server_name.lower().replace(' ', '_'),
                                   # compose_project_directory=path.dirname(self.compose_file),
                                   compose_project_directory=self.working_directory,
                                   )
        super().__init__(server_name)

    @classmethod
    def _mutate_to_proper_compose_file(cls) -> str:
        with open(cls.compose_file, 'r') as compose_file:
            compose_contents = yaml.safe_load(compose_file)

        assert 'services' in compose_contents, 'How can we have a server, without any docker-compose services'
        for service in compose_contents['services'].values():
            try:
                del service['container_name']  # container_name overrules our project_name prefix, so it has to go!
            except KeyError:
                continue

        assert ' ' not in cls.game_name, "Guess we shouldn't use .game_name after all"
        mutated_compose_path: str = path.join(COMPOSE_FILES_DIR, f"{cls.game_name}.yml")
        with open(mutated_compose_path, 'w') as mutated_compose_file:
            mutated_compose_file.write(  "# WARNING DO NOT EDIT, YOUR CHANGES WILL BE LOST.\n"
                                         "# THIS FILE HAS BEEN MUTATED FROM THE ORIGINAL\n"
                                        f"# FOUND HERE: {cls.compose_file}\n\n")
            yaml.safe_dump(compose_contents, mutated_compose_file)
        return mutated_compose_path

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

        # ._mutate_to_proper_compose_file() creates a compose-file in another directory,
        # but python-on-whales should continue to use the directory of the original compose-file.
        cls.working_directory = path.dirname(cls.compose_file)
        cls.compose_file = cls._mutate_to_proper_compose_file()

    def start(self):
        # TODO Kevin: .start() or .up()? I dont know.
        self.client.compose.up(detach=True, services=list(self.services))

    def stop(self):
        # TODO Kevin: .stop() or .down()? I dont know.
        self.client.compose.stop()

    def is_running(self) -> bool:
        # TODO Kevin: What if the server has multiple services?
        raise NotImplementedError

    def set_version(self, version: str):
        self.restart()

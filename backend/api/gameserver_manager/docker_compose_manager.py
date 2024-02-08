from __future__ import annotations

import os
from os import path
from os import PathLike
from pathlib import Path

import yaml
from abc import ABC
from typing import Iterable

from api.gameserver_manager.github_versioned_manager import GitHubVersionedManager

PORT_MAX: int = 2**16

try:
    from python_on_whales import DockerClient, Container, Network, DockerException
    from python_on_whales.components.container.cli_wrapper import ValidPortMapping
except (ModuleNotFoundError, ImportError) as e:
    raise ModuleNotFoundError(f"Failed to import python_on_whales, install with 'pip3 install python_on_whales'") from e

from api.gameserver_manager.base_manager import AbstractGameServerManager


COMPOSE_FILES_DIR: PathLike | str = 'compose_files/'


class AbstractDockerComposeGameServerManager(AbstractGameServerManager, ABC):
    compose_file: str = None
    _original_compose_file: str = None
    client: DockerClient
    services: list[str] | str = None  # services must be a list when multiple, because of python-on-whales reasons
    # ports: list[ValidPortMapping] = None

    def __init__(self, server_name: str) -> None:
        super().__init__(server_name)
        self._original_compose_file = self.compose_file
        self.compose_file = self._mutate_to_proper_compose_file()
        # TODO Kevin: Everything will most likely explode if the server_name/compose_project_name is changed.
        # TODO Kevin: Also, how can we make sure the project name prefix is applied to containers when container_name
        #   is specified in the docker-compose.yml file?
        # self.client = DockerClient(compose_files=[self.compose_file], compose_env_file= , compose_project_name=server_name)
        self.client = DockerClient(compose_files=[self.compose_file],
                                   compose_project_name=self.get_project_name(),
                                   # compose_project_directory=path.dirname(self.compose_file),
                                   compose_project_directory=self.working_directory,
                                   )

    def get_project_name(self):
        return self.server_name.lower().replace(' ', '_')

    def _get_game_compose_dir(self) -> Path:
        assert ' ' not in self.game_name, "Guess we shouldn't use .game_name after all"
        assert '/' not in self.game_name, "Guess we shouldn't use .game_name after all"
        return Path(COMPOSE_FILES_DIR, self.game_name)

    @staticmethod
    def scan_compose_ports(compose_dir: Path = Path(COMPOSE_FILES_DIR), recurse_depth: int = 0) -> set[int]:
        used_ports: set[int] = set()
        for file in compose_dir.iterdir():

            if file.parts[-1].startswith('.'):
                continue  # Ignore hidden files

            try:
                with open(file, 'r') as compose_file:
                    compose_contents = yaml.safe_load(compose_file)
            except IsADirectoryError:
                if recurse_depth > 0:
                    used_ports |= AbstractDockerComposeGameServerManager.scan_compose_ports(file, recurse_depth-1)
                continue
            except OSError:
                continue

            if 'services' not in compose_contents:
                continue  # This is probably not a docker-compose file

            for service in compose_contents['services'].values():
                ports: list[str] = service['ports']
                assert isinstance(ports, list)
                # ports:
                # - 42420: 42420
                # - 42421: 42421
                # - 42422: 42422
                for port_pair in ports:
                    #   vvvvv
                    # - 42420: 42420
                    host_port: int = int(port_pair.split(':')[0])
                    used_ports.add(host_port)

        return used_ports

    def ports_used(self) -> dict[str, list[str]]:

        with open(self.compose_file, 'r') as compose_file:
            compose_contents = yaml.safe_load(compose_file)
        assert 'services' in compose_contents, 'How can we have a server, without any docker-compose services'

        return {service_name: service.get('ports', []) for service_name, service in compose_contents['services'].items()}

    @staticmethod
    def _fit_available_ports(our_compose: dict) -> None:
        used_ports: set[int] = AbstractDockerComposeGameServerManager.scan_compose_ports(recurse_depth=2)

        for service in our_compose['services'].values():
            try:
                old_ports: list[str] = service['ports']
            except KeyError:
                continue
            new_ports: list[str] = []
            for port_pair in old_ports:
                desired_host_port, inner_port = port_pair.split(':')
                desired_host_port, inner_port = int(desired_host_port), int(inner_port)

                # Keep incrementing from the desired port, until we find one that is actually available.
                # TODO Kevin: Also check that the port is currently OS available.
                new_ports.append(f"{next(port for port in range(desired_host_port, PORT_MAX) if port not in used_ports)}:{inner_port}")

            service['ports'] = new_ports  # Replace old desired ports with the actually available ones

    def _mutate_to_proper_compose_file(self) -> str:
        # assert ' ' not in self.server_name, "Guess we shouldn't use .server_name after all"
        assert '/' not in self.server_name, "Guess we shouldn't use .server_name after all"
        qual_server_name = self.server_name.replace(' ', '_')
        mutated_compose_path: Path = Path(self._get_game_compose_dir(), f"{qual_server_name}.yml")
        mutated_compose_path.parent.mkdir(exist_ok=True, parents=True)

        # Guard clause
        if mutated_compose_path.is_file():
            # Return the already existing mutated compose file.
            return str(mutated_compose_path)

        with open(self._original_compose_file, 'r') as compose_file:
            compose_contents = yaml.safe_load(compose_file)

        assert 'services' in compose_contents, 'How can we have a server, without any docker-compose services'
        # An alternative approach could be:
        #for container in self.client.compose.ps(services=self.services):
        #    container.rename()

        if self.services:
            for service in set(compose_contents['services'].keys()):
                if service not in self.services:
                    del compose_contents['services'][service]

        for service in compose_contents['services'].values():
            try:
                del service['container_name']  # container_name overrules our project_name prefix, so it has to go!
            except KeyError:
                continue

        self._fit_available_ports(compose_contents)

        # Recreate the mutated compose file.
        with open(mutated_compose_path, 'w') as mutated_compose_file:
            mutated_compose_file.write(  "# WARNING DO NOT EDIT, YOUR CHANGES WILL BE LOST.\n"
                                         "# THIS FILE HAS BEEN MUTATED FROM THE ORIGINAL\n"
                                        f"# FOUND HERE: {self.compose_file}\n\n")
            yaml.safe_dump(compose_contents, mutated_compose_file)
        return str(mutated_compose_path)

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

    def start(self):
        # TODO Kevin: Container will obviously fail to start,
        #   if the port is already in use by another server.
        # TODO Kevin: .start() or .up()? I dont know.
        self.client.compose.up(detach=True, services=list(self.services))

    def stop(self):
        # TODO Kevin: .stop() or .down()? I dont know.
        self.client.compose.stop()

    def restart(self):
        self.client.compose.restart()

    def server_running(self) -> bool | None:
        """ Currently returns True if any specified services are running, otherwise False. """

        # TODO Kevin: What if the server has multiple services?
        try:
            return bool(self.client.compose.ps(self.services))
        except DockerException:
            return None

    def delete(self):
        self.client.compose.down()
        try:
            os.remove(self.compose_file)
        except FileNotFoundError:
            pass


class GitHubVersionedDockerComposeManager(GitHubVersionedManager, AbstractDockerComposeGameServerManager, ABC):

    def set_version(self, version: str):
        super(GitHubVersionedDockerComposeManager, self).set_version(version)
        #self.stop()
        self.client.compose.build()  # TODO Kevin: Is a full rebuild required?
        #self.start()

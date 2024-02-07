from __future__ import annotations

from os import PathLike
from typing import Type, Iterable, Sequence
from abc import ABC, abstractmethod


class AbstractGameServerManager(ABC):

    game_name: str

    server_name: str  # TODO Kevin: This should probably update if the container name on the Model does.
    working_directory: PathLike[str] | str = None

    def __init__(self, server_name: str) -> None:
        self.server_name = server_name
        super().__init__()

    def __init_subclass__(cls) -> None:
        cls.game_name = cls.__name__.removesuffix('Manager')
        super().__init_subclass__()

        # Only non-abstract classes should be registered to the manager dictionary.
        # They may be better ways to check if the subclass is still abstract.
        #   What if the user doesn't know to subclass ABC ?
        #   inspect.isabstract() doesn't appear to work for AbstractDockerComposeGameServer sadly
        if ABC in cls.__bases__:
            return

        assert cls.game_name not in managers, 'Game name should be unique'
        # TODO Kevin: This will explode into a thousand pieces if we change the key while we have rows in the database.
        #   Perhaps we should use Django-polymorphism (or similar) instead.
        managers[cls.game_name] = cls

    def make_savefile_backup(self):
        # TODO Kevin: We can definitely run out of space here
        raise NotImplementedError

    @abstractmethod
    def start(self):
        raise NotImplementedError

    @abstractmethod
    def stop(self):
        raise NotImplementedError

    def restart(self):
        self.stop()
        self.start()

    def get_player_count(self) -> int:
        raise NotImplementedError

    def get_players(self):
        raise NotImplementedError

    @abstractmethod
    def server_running(self) -> bool | None:
        raise NotImplementedError

    def server_running(self) -> bool:
        raise NotImplementedError


managers: dict[str, Type[AbstractGameServerManager]] = {}


# def test():
#     client = docker.from_env()
#     # lst = client.containers.list()
#     this: Container = client.containers.get("tverfagligt_api_1")
#     this.remove(force=True)
#
#     for i in range(10):
#         print('AAA')
#
#     # client.containers.run("bfirsh/reticulate-splines", detach=True)

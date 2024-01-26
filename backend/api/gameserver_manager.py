from typing import Type
from abc import ABC, abstractmethod


class AbstractGameServerManager(ABC):

    game_name: str
    server_name: str  # TODO Kevin: This should probably update if the container name on the Model does.

    def __init__(self, server_name: str) -> None:
        self.server_name = server_name
        super().__init__()

    def __init_subclass__(cls) -> None:
        cls.game_name = cls.__name__.removesuffix('Manager')
        super().__init_subclass__()
        # They may be better ways to check if the subclass is still abstract.
        #   What if the user doesn't know to subclass ABC ?
        if ABC in cls.__bases__:
            return
        assert cls.game_name not in managers, 'Game name should be unique'
        # TODO Kevin: This will explode into a thousand pieces if we change the key while we have rows in the database.
        #   Perhaps we should use Django-polymorphism (or similar) instead.
        managers[cls.game_name] = cls

    def make_savefile_backup(self):
        # TODO Kevin: We can definitely run out of space here
        raise NotImplementedError

    def update_version(self, version=None):
        raise NotImplementedError

    @abstractmethod
    def start(self):
        raise NotImplementedError

    @abstractmethod
    def stop(self):
        raise NotImplementedError

    def get_player_count(self):
        raise NotImplementedError

    def get_players(self):
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

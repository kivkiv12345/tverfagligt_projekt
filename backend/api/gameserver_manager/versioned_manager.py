from abc import ABC, abstractmethod
from typing import Iterable, Sequence

from api.gameserver_manager.base_manager import AbstractGameServerManager


class VersionedGameServerManager(AbstractGameServerManager, ABC):

    game_versions: Sequence[str] = ()

    def __init_subclass__(cls) -> None:
        super().__init_subclass__()

        # Only non-abstract classes should be registered to the manager dictionary.
        # They may be better ways to check if the subclass is still abstract.
        #   What if the user doesn't know to subclass ABC ?
        #   inspect.isabstract() doesn't appear to work for AbstractDockerComposeGameServer sadly
        if ABC in cls.__bases__:
            return

        assert cls.game_versions, 'A versioned manager should probably have some versions'

    @abstractmethod
    def get_version(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def set_version(self, version: str):
        raise NotImplementedError

    @property
    def available_versions(self) -> Iterable[str]:
        return self.game_versions

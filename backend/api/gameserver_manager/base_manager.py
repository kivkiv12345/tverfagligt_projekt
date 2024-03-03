from __future__ import annotations

from dataclasses import dataclass
from os import PathLike
from abc import ABC, abstractmethod
from typing import Type, NamedTuple

from rest_framework import status
from rest_framework.response import Response
from typing import TYPE_CHECKING

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

if TYPE_CHECKING:
    from django.contrib.auth.models import User, AnonymousUser

    from api.models import ServerEvent, GameServer, ServerEventChoices, \
        ServerPermission, ServerPermissionChoices


# TODO Kevin: I can't really decide what return value pattern feels best here.
def server_from_identifier(identifier: int | str | GameServer) -> GameServer | Response:
    """

    :returns: A GameServer if a valid identifier was specified, otherwise Response with error-code set
    """

    # TODO Kevin: Circular import!
    from api.models import GameServer

    if isinstance(identifier, GameServer):
        return identifier

    if isinstance(identifier, int):
        try:
            return GameServer.objects.get(pk=identifier)
        except GameServer.DoesNotExist:
            return Response(f"Server with ID '{identifier}' could not be found", status=status.HTTP_404_NOT_FOUND)

    if isinstance(identifier, str):
        try:
            return GameServer.objects.get(server_name=identifier)
        except GameServer.DoesNotExist:
            return Response(f"Server with name '{identifier}' could not be found", status=status.HTTP_404_NOT_FOUND)

    raise TypeError(f"type {type(identifier)} is not a valid identifier for GameServer")


def websocket_notify_server_opened(server_ident: int | str | GameServer):
    """ Notify connected clients about server status change via WebSocket """

    server_id = server_from_identifier(server_ident).pk

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        # TODO Kevin: Ensure message enums are identical to frontend by putting in library.
        f"server_{server_id}", {"type": "server_event", "message": "Server opened"}
    )


def websocket_notify_serer_closed(server_ident: int | str | GameServer):
    """ Notify connected clients about server status change via WebSocket """

    server_id = server_from_identifier(server_ident).pk

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        # TODO Kevin: Ensure message enums are identical to frontend by putting in library.
        f"server_{server_id}", {"type": "server_event", "message": "Server closed"}
    )


@dataclass(init=True)
class ServerPermissionError(PermissionError):
    # TODO Kevin: Should we allow None?
    response: Response
    # response: Response | None


def validate_server_permission(server: GameServer | int, user: User) -> Response | None:
    """
    Check if a given has permission to control the specified server.

    :returns: a Response instance with a status code set,
        if the user lacks permissions for the specified server, otherwise None.
    """
    # TODO Kevin: Unit test this.

    # TODO Kevin: Circular import!
    from django.contrib.auth.models import User, AnonymousUser
    from api.models import ServerPermission, ServerPermissionChoices

    if isinstance(server := server_from_identifier(server), Response):
        return server

    try:
        # TODO Kevin: This will create 2 queries, so is bad.
        if isinstance(user, AnonymousUser):
            raise ServerPermission.DoesNotExist
        user_permission: ServerPermission = ServerPermission.objects.get(user=user, server=server)
        if user_permission.access == ServerPermissionChoices.ALLOW:
            return None  # User has permissions for this server
        elif user_permission.access == ServerPermissionChoices.DENY:
            return Response(status=status.HTTP_403_FORBIDDEN)
    except User.DoesNotExist:
        # I think it's very unlikely that the user doesn't exist.
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    except ServerPermission.DoesNotExist:  # No override persmission specified between this server and user.
        if server.default_permissions == ServerPermissionChoices.ALLOW:
            return None
        return Response(status=status.HTTP_403_FORBIDDEN)

    assert False, "With how the validation function is structured, it shouldn't be possible to reach a default here."


class AbstractGameServerManager(ABC):

    game_name: str

    # NOTE Kevin: This creates a cyclic reference which requires the garbage collector
    server: GameServer  # TODO Kevin: This should probably update if the container name on the Model does.
    working_directory: PathLike[str] | str = None

    @property
    def server_name(self) -> str:
        return self.server.server_name

    def __init__(self, server: GameServer) -> None:
        self.server = server
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
    def start(self, user: User = None):

        # TODO Kevin: Circular import!
        from api.models import ServerEvent, ServerEventChoices

        # Check if the user has permission for the server
        if isinstance(permission_error := validate_server_permission(self.server, user), Response):
            raise ServerPermissionError(permission_error)

        ServerEvent.objects.create(user=user, server=self.server, type=ServerEventChoices.ENABLE)
        websocket_notify_server_opened(self.server)

    @abstractmethod
    def stop(self, user: User = None):

        # TODO Kevin: Circular import!
        from api.models import ServerEvent, ServerEventChoices

        # Check if the user has permission for the server
        if isinstance(permission_error := validate_server_permission(self.server, user), Response):
            raise ServerPermissionError(permission_error)

        ServerEvent.objects.create(user=user, server=self.server, type=ServerEventChoices.DISABLE)
        websocket_notify_serer_closed(self.server)

    def restart(self, user: User = None):
        self.stop(user)
        self.start(user)

    def get_player_count(self) -> int:
        raise NotImplementedError

    def get_players(self):
        raise NotImplementedError

    @abstractmethod
    def server_running(self) -> bool | None:
        raise NotImplementedError

    def delete(self):
        """ Delete the associated server(s) """
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

from __future__ import annotations

from typing import NamedTuple, Any

from django.contrib.auth import logout, authenticate
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.request import Request
from rest_framework.response import Response
from django.contrib.auth.models import User, AnonymousUser

from api.models import ServerPermission, GameServer, ServerPermissionChoices


# Create your views here.
@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
def get_server_info(request: Request) -> Response:
    raise NotImplementedError
    return Response(status=status.HTTP_204_NO_CONTENT)


# class Result(NamedTuple):
#     data: Any
#     err_resp: Response


# TODO Kevin: I can't really decide what return value pattern feels best here.
def server_from_identifier(identifier: int | str | GameServer) -> GameServer | Response:
    """

    :returns: A GameServer if a valid identifier was specified, otherwise Response with error-code set
    """

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


def validate_server_permission(server: GameServer | int, user: User) -> Response | None:
    """
    Check if a given has permission to control the specified server.

    :returns: a Response instance with a status code set,
        if the user lacks permissions for the specified server, otherwise None.
    """
    # TODO Kevin: Unit test this.

    if isinstance(server := server_from_identifier(server), Response):
        return server

    try:
        # TODO Kevin: This will create 2 queries, so is bad.
        if isinstance(user, AnonymousUser):
            raise ServerPermission.DoesNotExist
        user_permission: ServerPermission = ServerPermission.objects.get(user=user, server=server)
        if user_permission.access is ServerPermissionChoices.ALLOW:
            return None  # User has permissions for this server
        elif user_permission.access is ServerPermissionChoices.DENY:
            return Response(status=status.HTTP_403_FORBIDDEN)
    except User.DoesNotExist:
        # I think it's very unlikely that the user doesn't exist.
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    except ServerPermission.DoesNotExist:  # No override persmission specified between this server and user.
        if server.default_permissions == ServerPermissionChoices.ALLOW:
            return None
        return Response(status=status.HTTP_403_FORBIDDEN)

    assert False, "With how the validation function is structured, it shouldn't be possible to reach a default here."


@api_view(['POST'])
def backup_savefile(request: Request) -> Response:
    """

    Expected JSON:
    {
        "server_ident": int | str,
    }
    """

    data = request.data

    server_ident = data.get('server_ident')
    if server_ident is None:
        return Response("Must specify 'server_ident' in request", status=status.HTTP_400_BAD_REQUEST)

    # Find server from name or ID
    if isinstance(server := server_from_identifier(server_ident), Response):
        return server

    # Check if the user has permission to stop the server
    if error_response := validate_server_permission(server, request.user):
        return error_response

    server.manager.make_savefile_backup()  # TODO Kevin: Error handling here?

    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def stop_server(request: Request) -> Response:
    """

    Expected JSON:
    {
        "server_ident": int | str,
    }
    """

    data = request.data

    server_ident = data.get('server_ident')
    if server_ident is None:
        return Response("Must specify 'server_ident' in request", status=status.HTTP_400_BAD_REQUEST)

    # Find server from name or ID
    if isinstance(server := server_from_identifier(server_ident), Response):
        return server

    # Check if the user has permission for the server
    if error_response := validate_server_permission(server, request.user):
        return error_response

    server.manager.stop()  # TODO Kevin: Error handling here?

    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def start_server(request: Request) -> Response:
    """

    Expected JSON:
    {
        "server_ident": int | str,
    }
    """

    data = request.data

    server_ident = data.get('server_ident')
    if server_ident is None:
        return Response("Must specify 'server_ident' in request", status=status.HTTP_400_BAD_REQUEST)

    # Find server from name or ID
    if isinstance(server := server_from_identifier(server_ident), Response):
        return server

    # Check if the user has permission for the server
    if error_response := validate_server_permission(server, request.user):
        return error_response

    server.manager.start()  # TODO Kevin: Error handling here?

    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def set_server_version(request: Request) -> Response:
    """

    Expected JSON:
    {
        "server_ident": int | str,
        "server_version": str,
    }
    """

    data = request.data

    server_ident = data.get('server_ident')
    if server_ident is None:
        return Response("Must specify 'server_ident' in request", status=status.HTTP_400_BAD_REQUEST)

    server_version = data.get('server_version')
    if server_version is None:
        return Response("Must specify 'server_version' in request", status=status.HTTP_400_BAD_REQUEST)

    # Find server from name or ID
    if isinstance(server := server_from_identifier(server_ident), Response):
        return server

    # Check if the user has permission for the server
    if error_response := validate_server_permission(server, request.user):
        return error_response

    try:
        server.manager.set_version(server_version)
    except KeyError as e:  # TODO Kevin: Are we revealing to much information here?
        return Response(str(e), status.HTTP_400_BAD_REQUEST)

    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def get_server_version(request: Request, ident: str) -> Response:
    """

    Expected JSON:
    {
        "server_ident": int | str,
    }
    """

    data = request.data

    # server_ident = data.get('server_ident')
    server_ident = ident
    if server_ident is None:
        return Response("Must specify 'server_ident' in request", status=status.HTTP_400_BAD_REQUEST)

    try:
        server_ident = int(server_ident)  # ident must be PK
    except ValueError:
        pass  # ident should be server name

    # Find server from name or ID
    if isinstance(server := server_from_identifier(server_ident), Response):
        return server

    # TODO Kevin: Check if server supports multiple versions.

    # Check if the user has permission for the server
    # TODO Kevin: We may want to keep some servers 'secret',
    #   but otherwise must people should probably be allowed to check versions.
    if error_response := validate_server_permission(server, request.user):
        return error_response

    # TODO Kevin: Should probably be JSON
    return Response(server.manager.get_version(), status=status.HTTP_200_OK)


@api_view(['GET'])
def is_server_running(request: Request, ident: str) -> Response:
    """

    Expected JSON:
    {
        "server_ident": int | str,
    }
    """

    data = request.data

    # server_ident = data.get('server_ident')
    server_ident = ident
    if server_ident is None:
        return Response("Must specify 'server_ident' in request", status=status.HTTP_400_BAD_REQUEST)

    try:
        server_ident = int(server_ident)  # ident must be PK
    except ValueError:
        pass  # ident should be server name

    # Find server from name or ID
    if isinstance(server := server_from_identifier(server_ident), Response):
        return server

    # Check if the user has permission for the server
    # TODO Kevin: We may want to keep some servers 'secret',
    #   but otherwise must people should probably be allowed to check versions.
    if error_response := validate_server_permission(server, request.user):
        return error_response

    # TODO Kevin: Should probably be JSON
    return Response(server.manager.server_running(), status=status.HTTP_200_OK)


# With inspiration from https://chat.openai.com
@api_view(['POST'])
def user_login(request: Request) -> Response:
    """
    Expected JSON:
    {
        "username": str,
        "password": str
    }
    """

    data: dict = request.data

    username: str = data.get('username')
    password: str = data.get('password')

    if None in (username, password):
        return Response('Request must include both "username" and "password"', status=status.HTTP_400_BAD_REQUEST)

    user: User | None = authenticate(request, username=username, password=password)

    if user is None:
        return Response('Invalid username or password', status=status.HTTP_400_BAD_REQUEST)

    if not user.is_active:
        return Response('User is disabled', status=status.HTTP_400_BAD_REQUEST)

    token, created = Token.objects.get_or_create(user=user)
    return Response({'token': token.key}, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
def user_logout(request: Request) -> Response:
    """
    Expected JSON:
    {
        "token": str,
    }
    """

    request.user.auth_token.delete()
    logout(request.user)
    return Response({'detail': 'Logged out successfully.'}, status=status.HTTP_200_OK)

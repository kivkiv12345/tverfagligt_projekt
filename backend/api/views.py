from __future__ import annotations

from typing import NamedTuple, Any

from django.contrib.auth import logout, authenticate, login
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from django.contrib.auth.models import User, AnonymousUser

from api.gameserver_manager.base_manager import validate_server_permission, server_from_identifier, \
    ServerPermissionError
from api.models import GameServer
from api.serializers import GameServerSerializer


# Create your views here.
@api_view(['GET'])
# @authentication_classes([SessionAuthentication, TokenAuthentication])  # TODO Kevin: CSRF token
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_server_info(request: Request) -> Response:
    # TODO Kevin: validate_server_permission() should be implemented as a query for performance reasons.
    servers = (server for server in GameServer.objects.all() if not isinstance(validate_server_permission(server, request.user), Response))
    serializer = GameServerSerializer(servers, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


ERROR_KEY = 'error'


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
        return Response({ERROR_KEY: "Must specify 'server_ident' in request"}, status=status.HTTP_400_BAD_REQUEST)

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
    Stop the specified server. This shouldn't delete saves, progress, etc.
    Response time may be very long (>10 seconds), depending on the server/backend.

    Expected JSON:
    {
        "server_ident": int | str,
    }
    """

    data = request.data

    server_ident = data.get('server_ident')
    if server_ident is None:
        return Response({ERROR_KEY: "Must specify 'server_ident' in request"}, status=status.HTTP_400_BAD_REQUEST)

    # Find server from name or ID
    if isinstance(server := server_from_identifier(server_ident), Response):
        return server

    try:
        server.manager.stop(request.user)  # TODO Kevin: Error handling here?
    except ServerPermissionError as e:
        return e.response

    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def start_server(request: Request) -> Response:
    """
    Start the specified server. Should create a new one if required.
    Response time may be very long (>10 seconds), depending on the server/backend.

    Expected JSON:
    {
        "server_ident": int | str,
    }
    """

    data = request.data

    server_ident = data.get('server_ident')
    if server_ident is None:
        return Response({ERROR_KEY: "Must specify 'server_ident' in request"}, status=status.HTTP_400_BAD_REQUEST)

    # Find server from name or ID
    if isinstance(server := server_from_identifier(server_ident), Response):
        return server

    try:
        server.manager.start(request.user)  # TODO Kevin: Error handling here?
    except ServerPermissionError as e:
        return e.response

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
        return Response({ERROR_KEY: "Must specify 'server_ident' in request"}, status=status.HTTP_400_BAD_REQUEST)

    server_version = data.get('server_version')
    if server_version is None:
        return Response({ERROR_KEY: "Must specify 'server_version' in request"}, status=status.HTTP_400_BAD_REQUEST)

    # Find server from name or ID
    if isinstance(server := server_from_identifier(server_ident), Response):
        return server

    # Check if the user has permission for the server
    if error_response := validate_server_permission(server, request.user):
        return error_response

    try:
        server.manager.set_version(server_version)
    except KeyError as e:  # TODO Kevin: Are we revealing to much information here?
        return Response({ERROR_KEY: str(e)}, status.HTTP_400_BAD_REQUEST)

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
        return Response({ERROR_KEY: "Must specify 'server_ident' in request"}, status=status.HTTP_400_BAD_REQUEST)

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
    return Response({'server_version': server.manager.get_version()}, status=status.HTTP_200_OK)


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
        return Response({ERROR_KEY: "Must specify 'server_ident' in request"}, status=status.HTTP_400_BAD_REQUEST)

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

    return Response({'is_running': server.manager.server_running()}, status=status.HTTP_200_OK)


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
        return Response({ERROR_KEY: 'Request must include both "username" and "password"'}, status=status.HTTP_400_BAD_REQUEST)

    user: User | None = authenticate(request, username=username, password=password)

    if user is None:
        return Response({ERROR_KEY: 'Invalid username or password'}, status=status.HTTP_400_BAD_REQUEST)

    if not user.is_active:
        return Response({ERROR_KEY: 'User is disabled'}, status=status.HTTP_400_BAD_REQUEST)

    login(request, user)
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
    logout(request)
    return Response({'detail': 'Logged out successfully.'}, status=status.HTTP_200_OK)

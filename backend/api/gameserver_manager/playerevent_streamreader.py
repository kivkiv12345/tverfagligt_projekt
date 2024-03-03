from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime
from sys import stderr
from threading import Thread, Event
from typing import NamedTuple, Callable, Iterable

import re
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from django.contrib.auth.models import User
    from api.models import GameServer

from api.gameserver_manager.base_manager import AbstractGameServerManager


class PlayerEventSubscriber(NamedTuple):
    on_player_join: Callable[[str], None]
    on_player_leave: Callable[[str], None]


# TODO Kevin: Consider lifetime implications of this class
class PlayerEventStreamReader(AbstractGameServerManager, ABC):

    subscribers: list[PlayerEventSubscriber] = None
    listener_thread: Thread = None
    stop_flag: Event = None

    joined_players: list[str] = None

    player_join_pattern: re.Pattern = None
    player_leave_pattern: re.Pattern = None
    #log_func: Callable

    def __init_subclass__(cls) -> None:
        super().__init_subclass__()

        # Only non-abstract classes should be registered to the manager dictionary.
        # They may be better ways to check if the subclass is still abstract.
        #   What if the user doesn't know to subclass ABC ?
        #   inspect.isabstract() doesn't appear to work for AbstractDockerComposeGameServer sadly
        if ABC in cls.__bases__:
            return

        assert cls.player_join_pattern, 'Must have a capture group for when a player joins'
        assert cls.player_leave_pattern, 'Must have a capture group for when a player leaves'
        #assert cls.log_func, 'Must have a function to call that streams logs to read'

    def _follow_logs(self):
        #for stream_type, stream_content in self.log_func():
        # TODO Kevin: This is hardcoded to Docker Compose, so is bad
        for stream_type, stream_content in self.client.compose.logs(follow=True, stream=True, since='0m'):
        # for stream_type, stream_content in self.client.compose.logs(follow=True, stream=True):

            if stream_type == 'stdin':
                continue

            if self.stop_flag.is_set():  # Server is stopping, all client will be disconnected
                for player in self.joined_players:
                    self.on_player_leave(player)
                    try:
                        self.joined_players.remove(player)
                    except ValueError:
                        pass
                return

            # A bit of help from ChatGPT with the regex capture-groups here.

            # Match player join event
            join_match = self.player_join_pattern.match(stream_content.decode())
            if join_match:
                print(stream_content.decode())
                self.joined_players.append(join_match.group(1))
                self.on_player_join(join_match.group(1))
                continue  # Players can't both join and leave on the same line

            # Match player leave event
            leave_match = self.player_leave_pattern.match(stream_content.decode())
            if leave_match:
                print(stream_content.decode())
                try:
                    self.joined_players.remove(leave_match.group(1))
                except ValueError:
                    pass
                self.on_player_leave(leave_match.group(1))

    def __init__(self, server: GameServer) -> None:
        self.subscribers = []
        self.stop_flag = Event()
        self.listener_thread = Thread(target=self._follow_logs)
        self.joined_players = []
        super().__init__(server)
        if self.server_running():
            try:
                pass#self.listener_thread.run()  # TODO Kevin: Hangs forever for some reason
            except RuntimeError as e:
                stderr.write(str(e))

    def on_player_join(self, player_name: str):
        for listener in self.subscribers:
            listener.on_player_join(player_name)

    def on_player_leave(self, player_name: str):
        for listener in self.subscribers:
            listener.on_player_leave(player_name)

    def subscribe(self, subscription: PlayerEventSubscriber):
        self.subscribers.append(subscription)

    def start(self, user: User = None):
        super().start(user)
        try:
            self.listener_thread.run()
        except RuntimeError as e:
            stderr.write(str(e))

    def stop(self, user: User = None):
        super().stop(user)
        self.stop_flag.set()

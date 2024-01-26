from typing import Type

from django.db import models
from django.contrib.auth.models import User
from django.db.models import Model, ForeignKey, CASCADE, TextChoices, CharField, UniqueConstraint, PositiveIntegerField, \
    DateTimeField
from django.db.models.functions import Lower

from api.gameserver_manager import AbstractGameServerManager, managers


class StrChoicesEnum(TextChoices):
    @classmethod
    def max_choice_len(cls):
        # C has fueled my paranoia, so we do +1 on the length
        return len(max(cls, key=lambda choice: len(str(choice)))) + 1


class ServerPermissionChoices(StrChoicesEnum):
    # TODO Kevin: Should we handle separate permissions for start/stop, making backups, etc?
    ALLOW = 'ALLOW'
    DENY = 'DENY'

# TODO Kevin: How best to get GameServer containers on the same Docker network as Django?


class GameServer(Model):
    # TODO Kevin: Consider what happens when containers are deleted.
    # TODO Kevin: Could it make sense to subclass GameServer?
    #   Or should we make an Enum with managers?
    server_name = CharField(max_length=255)
    default_permissions = CharField(choices=ServerPermissionChoices.choices,
                                    max_length=ServerPermissionChoices.max_choice_len(),
                                    default=ServerPermissionChoices.DENY)
    # TODO Kevin: We may want to subclass a field here,
    #   which could probably give us a pretty way to get the manager and handle migrations.
    game = CharField(choices=[(game_name, game_name) for game_name in managers.keys()],
                     max_length=len(max(managers.values(), key=lambda manager: len(manager.__qualname__)).__qualname__) + 1,
                     null=False, blank=False)
    # version =

    manager: AbstractGameServerManager = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.pk:
            self.manager = managers[self.game](self.server_name)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super().save(force_insert, force_update, using, update_fields)
        # self.game was valid and has changed.
        if self.pk and type(self.manager) is not managers.get(self.game):
            # We don't really care for changing the game, but we support it for now.
            self.manager = managers[self.game](self.server_name)

    def __str__(self):
        return f"{self.game} | {self.server_name}"

    class Meta:
        constraints = [
            # Source: https://stackoverflow.com/questions/7773341/case-insensitive-unique-model-fields-in-django
            # server_name must be case-insensitive unique,
            # as we must convert it to lower case for python-on-whales to use it as a project name.
            # Which allows multiple servers to use the same docker-compose file.
            models.UniqueConstraint(
                Lower('server_name'),
                name='unique_ci_server_name'
            ),
        ]


class ServerEventChoices(StrChoicesEnum):
    ENABLE = 'ENABLE'
    DISABLE = 'DISABLE'


class ServerEvent(Model):
    type = CharField(choices=ServerEventChoices.choices, max_length=ServerEventChoices.max_choice_len())
    user = ForeignKey(User, on_delete=CASCADE, help_text='Shows which user caused this event')
    server = ForeignKey(GameServer, on_delete=CASCADE, help_text='Shows which server this event affected')
    timestamp = DateTimeField(auto_now_add=True, help_text='Shows when this event occurred')


class ServerPermission(Model):
    server = ForeignKey(GameServer, on_delete=CASCADE)
    user = ForeignKey(User, on_delete=CASCADE)
    access = CharField(choices=ServerPermissionChoices.choices, max_length=ServerPermissionChoices.max_choice_len(),
                       help_text='This is the final say for whether a user has permission to control a given server')

    class Meta:
        constraints = [
            # Ensure that each user can't have multiple conflicting permissions
            # overriding the default for a given server
            # TODO Kevin: Maybe unit-test this?
            UniqueConstraint(fields=('server', 'user'), name='unique_privilege')
        ]
        # unique_together can also be used, but I've tried this before,
        # and I don't belive it actually creates a composite key.
        # unique_together = ('server', 'user')

    def __str__(self):
        return f"{self.server} + {self.user} = {self.access}"

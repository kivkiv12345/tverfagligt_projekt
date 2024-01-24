from typing import Type

from django.db import models
from django.contrib.auth.models import User
from django.db.models import Model, ForeignKey, CASCADE, TextChoices, CharField, UniqueConstraint, PositiveIntegerField, \
    DateTimeField


class StrChoicesEnum(TextChoices):
    @classmethod
    def max_choice_len(cls):
        # C has fueled my paranoia, so we do +1 on the length
        return len(max(cls, key=lambda choice: len(str(choice)))) + 1


class ServerPermissionChoices(StrChoicesEnum):
    # TODO Kevin: Should we handle separate permissions for start/stop, making backups, etc?
    ALLOW = 'ALLOW'
    DENY = 'DENY'


class GameServer(Model):
    # TODO Kevin: Consider what happens when containers are deleted.
    # TODO Kevin: Could it make sense to subclass GameServer?
    container = CharField(max_length=255)
    default_permissions = CharField(choices=ServerPermissionChoices.choices,
                                    max_length=ServerPermissionChoices.max_choice_len(),
                                    default=ServerPermissionChoices.DENY)

    def make_savefile_backup(self):
        # TODO Kevin: We can definitely run out of space here
        raise NotImplementedError

    def update_version(self, version=None):
        raise NotImplementedError

    def start(self):
        raise NotImplementedError

    def stop(self):
        raise NotImplementedError

    def __str__(self):
        return self.container


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

from django.db import models
from django.contrib.auth.models import User
from django.db.models import Model, ForeignKey, CASCADE, TextChoices, CharField, UniqueConstraint


class GameServer(Model):
    # TODO Kevin: Consider what happens when containers are deleted.
    container = CharField(max_length=255)


class ServerEventChoices(TextChoices):
    ENABLE = 'ENABLE'
    DISABLE = 'DISABLE'


class ServerEvent(Model):
    type = CharField(choices=ServerEventChoices.choices)
    user = ForeignKey(User, on_delete=CASCADE)
    server = ForeignKey(GameServer, on_delete=CASCADE)


class ServerPermissionChoices(TextChoices):
    ALLOW = 'ALLOW'
    DISALLOW = 'DISALLOW'


class ServerPermission(Model):
    server = ForeignKey(GameServer, on_delete=CASCADE, primary_key=True)
    user = ForeignKey(User, on_delete=CASCADE, primary_key=True)
    access = CharField(choices=ServerPermissionChoices.choices,
                       help_text='This is the final say for whether a given '
                                 'user has permission to control a given server')

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

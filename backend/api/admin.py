from django.contrib import admin
from django.contrib.admin import ModelAdmin

from api.models import GameServer, ServerPermission, ServerEvent


# Register your models here.
class GameServerAdmin(ModelAdmin):
    model = GameServer
    # fields = ['__all__']


class ServerPermissionAdmin(ModelAdmin):
    model = ServerPermission


class ServerEventAdmin(ModelAdmin):
    model = ServerEvent
    readonly_fields = ['timestamp']


admin.site.register(GameServer, GameServerAdmin)
admin.site.register(ServerPermission, ServerPermissionAdmin)
admin.site.register(ServerEvent, ServerEventAdmin)

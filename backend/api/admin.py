from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.db.models import QuerySet
from requests import Request

from api.models import GameServer, ServerPermission, ServerEvent


@admin.action(description="Start multiple servers")
def start_servers(modeladmin: ModelAdmin, request: Request, queryset: QuerySet[GameServer]):
    for server in queryset:
        server.manager.start()


@admin.action(description="Stop multiple servers")
def stop_servers(modeladmin: ModelAdmin, request: Request, queryset: QuerySet[GameServer]):
    for server in queryset:
        server.manager.stop()


# Register your models here.
class GameServerAdmin(ModelAdmin):
    model = GameServer
    # fields = *(field.name for field in GameServer._meta.get_fields()),
    readonly_fields = ['server_version']
    actions = [start_servers]


class ServerPermissionAdmin(ModelAdmin):
    model = ServerPermission


class ServerEventAdmin(ModelAdmin):
    model = ServerEvent
    readonly_fields = ['timestamp']


admin.site.register(GameServer, GameServerAdmin)
admin.site.register(ServerPermission, ServerPermissionAdmin)
admin.site.register(ServerEvent, ServerEventAdmin)

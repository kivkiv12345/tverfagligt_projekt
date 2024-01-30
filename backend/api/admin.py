from django import forms
from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.db.models import QuerySet
from django.forms import ModelForm
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
    actions = [start_servers]

    def get_form(self, request, obj: GameServer = None, change=False, **kwargs):
        if not obj:
            return super().get_form(request, obj, change, **kwargs)

        class GameServerAdminForm(ModelForm):
            CHOICES = ((game_version, game_version) for game_version in obj.manager.available_versions)
            server_version = forms.ChoiceField(choices=CHOICES, initial=obj.server_version)
            server_running = forms.BooleanField(initial=obj.manager.server_running(), required=False)

            class Meta:
                model = GameServer
                fields = '__all__'

        return GameServerAdminForm

    def save_model(self, request, obj: GameServer, form, change):
        assert 'server_version' in form.data
        new_version = form.data['server_version']
        should_run = 'server_running' in form.data
        if new_version != obj.server_version:
            obj.manager.set_version(new_version)
        if should_run != obj.manager.server_running():
            if should_run:
                obj.manager.start()
            else:
                obj.manager.stop()

        super().save_model(request, obj, form, change)


class ServerPermissionAdmin(ModelAdmin):
    model = ServerPermission


class ServerEventAdmin(ModelAdmin):
    model = ServerEvent
    readonly_fields = ['timestamp']


admin.site.register(GameServer, GameServerAdmin)
admin.site.register(ServerPermission, ServerPermissionAdmin)
admin.site.register(ServerEvent, ServerEventAdmin)

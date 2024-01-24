from django.urls import path

from api.views import start_server, get_server_info, backup_savefile, stop_server

urlpatterns = [
    path(f"get-server-info/", get_server_info, name="get-server-info"),
    path(f"backup-savefile/", backup_savefile, name="backup-savefile"),
    # path(f"card-move/", update, name="card-move"),
    path(f"stop-server/", stop_server, name="stop-server"),
    path(f"start-server/", start_server, name="start-server"),
]

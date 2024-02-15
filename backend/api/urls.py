from django.urls import path

from api.views import start_server, get_server_info, backup_savefile, stop_server, set_server_version, \
    get_server_version, is_server_running, user_logout, user_login
from rest_framework.authtoken import views as authviews

urlpatterns = [
    path(f"get-server-info/", get_server_info, name="get-server-info"),
    path(f"backup-savefile/", backup_savefile, name="backup-savefile"),
    # path(f"card-move/", update, name="card-move"),
    path(f"stop-server/", stop_server, name="stop-server"),
    path(f"start-server/", start_server, name="start-server"),
    path(f"set-server-version/", set_server_version, name="set-server-version"),
    path(f"get-server-version/<str:ident>", get_server_version, name="get-server-version"),
    path(f"is-server-running/<str:ident>", is_server_running, name="is-server-running"),

    path(f"token-auth/", authviews.obtain_auth_token),
    path(f"user-login/", user_login, name="user-login"),
    path(f"user-logout/", user_logout, name="user-logout"),
]

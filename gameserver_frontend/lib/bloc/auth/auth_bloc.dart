import 'package:dio/dio.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:gameserver_frontend/api.dart';
import 'package:gameserver_frontend/bloc/auth/auth_event.dart';
import 'package:gameserver_frontend/bloc/auth/auth_state.dart';
import 'package:gameserver_frontend/bloc/auth/user.dart';
import 'package:shared_preferences/shared_preferences.dart';


class AuthBloc extends Bloc<AuthEvent, AuthBlocState> {

  AuthBloc(super.initialState) {
    on<LoginEvent>(login);
    on<LogoutEvent>(logout);
    on<LoginFailureEvent>(login_failed);
  }

  factory AuthBloc.fromSharedPrefs(SharedPreferences prefs) {
    final String? token = prefs.getString('token');
    final String? username = prefs.getString('username');

    // Either we get both, or none.
    assert ((token == null && username == null) || (token != null && username != null));

    if (token != null && username != null) {
      return AuthBloc(LoggedInState(AuthenticatedUser.from_api(username, Api(token))));
    }

    return AuthBloc(LoggedOutState());
  }

  Future login(LoginEvent event, Emitter<AuthBlocState> emit) async {
    emit(LoggedInState(AuthenticatedUser.from_api(event.username, event.api)));
  }

  Future login_failed(LoginFailureEvent event, Emitter<AuthBlocState> emit) async {
    emit(LoginFailedState(event.username, event.message));
  }

  Future logout(LogoutEvent event, Emitter<AuthBlocState> emit) async {

    Response response = await event.user.logout();  // WebAPI call

    if (!bad_statuscode(response.statusCode)) {
      emit(LoggedOutState()); // Set state to stopped if stop successful
    } else {
      // emit(ServerErrorState()); // Something went wrong, now we don't know what's going on
    }

  }
}

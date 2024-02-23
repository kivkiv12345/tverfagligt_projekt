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
    //emit(ServerChangingState());  // Should disable the server widget

    // final response = await dio.post('$api_url/user-login/', data: {'server_ident': this.id});  // WebAPI call

    emit(LoggedInState(AuthenticatedUser.from_api(event.username, event.api)));  // Set state to started if start successful
    // if (!bad_statuscode(response.statusCode)) {
    //   emit(LoggedInState(AuthenticatedUser.from_api(event.username, event.api)));  // Set state to started if start successful
    // } else {
    //   emit(ServerErrorState());  // Something went wrong, now we don't know what's going on
    // }

  }

  // Future serverStarted(ServerStarted event, Emitter<ServerBlocState> emit) async {
  //   // TODO Kevin: Enable server widget
  //   emit(ServerRunningState());
  // }

  Future logout(LogoutEvent event, Emitter<AuthBlocState> emit) async {
    //emit(ServerChangingState());  // Should disable the server widget

    Response response = await event.user.logout();  // WebAPI call

    if (!bad_statuscode(response.statusCode)) {
      emit(LoggedOutState()); // Set state to stopped if stop successful
    } else {
      // emit(ServerErrorState()); // Something went wrong, now we don't know what's going on
    }

  }

  // Future serverStopped(ServerStopped event, Emitter<ServerBlocState> emit) async {
  //   // TODO Kevin: Enable server widget
  // }

  // Future serverChanging(ServerChanging event, Emitter<ServerBlocState> emit) async {

  // }
}

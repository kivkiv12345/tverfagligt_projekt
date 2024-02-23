import 'package:gameserver_frontend/api.dart';
import 'package:gameserver_frontend/bloc/auth/user.dart';

abstract class AuthEvent {}


class LoginEvent extends AuthEvent {

  Api api;
  String username;

  LoginEvent(this.api, this.username);

  static Future<LoginEvent> from_credentials(String username, String password) async {
    Api api = await Api.from_credentials(username, password);
    return LoginEvent(api, username);
  }
}

class LogoutEvent extends AuthEvent {
  final AuthenticatedUser user;

  LogoutEvent({required this.user});
}
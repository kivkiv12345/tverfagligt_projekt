import 'package:gameserver_frontend/exceptions.dart';
import 'package:gameserver_frontend/api.dart';
import 'package:gameserver_frontend/bloc/auth/user.dart';

abstract class AuthEvent {}


class LoginEvent extends AuthEvent {

  Api api;
  String username;

  LoginEvent(this.api, this.username);

  static Future<AuthEvent> from_credentials(String username, String password) async {
    try {
      Api api = await Api.from_credentials(username, password);
      return LoginEvent(api, username);
    } on PermissionDeniedError catch (e) {
      return LoginFailureEvent(username, e.message ?? "Login failed");
    }
  }
}

class LoginFailureEvent extends AuthEvent {
  String username;
  String message;

  LoginFailureEvent(this.username, this.message);

}

class LogoutEvent extends AuthEvent {
  final AuthenticatedUser user;

  LogoutEvent({required this.user});
}

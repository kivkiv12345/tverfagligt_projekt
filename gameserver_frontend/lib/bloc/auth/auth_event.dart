import 'package:gameserver_frontend/api.dart';
import 'package:gameserver_frontend/bloc/auth/user.dart';

abstract class AuthEvent {}


class LoginEvent extends AuthEvent {

  LoginEvent(Api api);

  static Future<LoginEvent> from_credentials(String username, String password) async {
    Api api = await Api.from_credentials(username, password);
    return LoginEvent(api);
  }
}

class LogoutEvent extends AuthEvent {
  final AuthenticatedUser user;

  LogoutEvent({required this.user});
}
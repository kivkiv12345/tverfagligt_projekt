import 'package:gameserver_frontend/bloc/auth/user.dart';

abstract class AuthBlocState {

  AuthBlocState();

}

class LoggedInState extends AuthBlocState {
  final AuthenticatedUser user;
  LoggedInState(this.user);
}

class LoggedOutState extends AuthBlocState {
  LoggedOutState();  // TODO Kevin: Should it be possible to signal which user has logged out?
}
import 'package:dio/dio.dart';
import 'package:gameserver_frontend/api.dart';

class User {
  final String username;

  User(this.username);
}

class AuthenticatedUser extends User {
  late final Api api;

  AuthenticatedUser(super.username, String token) {
    this.api = Api(token);
  }

  AuthenticatedUser.from_api(super.username, this.api);

  static Future<AuthenticatedUser> from_credentials(String username, String password) async {
    Api api = await Api.from_credentials(username, password);
    return AuthenticatedUser.from_api(username, api);
  }

  Future<Response> logout({
    Object? data,
    Map<String, dynamic>? queryParameters,
    Options? options,
    CancelToken? cancelToken,
    ProgressCallback? onSendProgress,
    ProgressCallback? onReceiveProgress,
  }) async {
    return this.api.logout();
  }
}
class ConnectionError implements Exception {
  String? message;

  ConnectionError([this.message]);
}

class PermissionDeniedError implements Exception {
  String? message;

  PermissionDeniedError([this.message]);
}
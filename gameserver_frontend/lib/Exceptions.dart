class ConnectionError implements Exception {
  String? message;

  ConnectionError([this.message]);
}
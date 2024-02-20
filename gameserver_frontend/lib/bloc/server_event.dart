import 'package:gameserver_frontend/ServerListWidget.dart';

abstract class ServerEvent {}


class ServerStart extends ServerEvent {
  final Server server;

  ServerStart(this.server);
}

class ServerStarted extends ServerEvent {
  final Server server;

  ServerStarted(this.server);
}

class ServerStopped extends ServerEvent {
  final Server server;

  ServerStopped(this.server);
}

class ServerStop extends ServerEvent {
  final Server server;

  ServerStop(this.server);
}

class ServerChanging extends ServerEvent {
  final Server server;

  ServerChanging(this.server);
}

class ServerError extends ServerEvent {
  final Server server;

  ServerError(this.server);
}

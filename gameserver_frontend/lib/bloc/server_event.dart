import 'package:gameserver_frontend/ServerListWidget.dart';

abstract class ServerEvent {}

class StartServer extends ServerEvent {
  final Server server;

  StartServer(this.server);
}

class StopServer extends ServerEvent {
  final Server server;

  StopServer(this.server);
}

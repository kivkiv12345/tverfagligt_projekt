import 'package:gameserver_frontend/ServerListWidget.dart';
import 'package:gameserver_frontend/bloc/server_state.dart';

abstract class ServerEvent {}

class ServerLoaded extends ServerEvent {
  ServerLoaded(this.state);
  final ServerState state;
}

class StartServer extends ServerEvent {
  final Server server;

  StartServer(this.server);
}

class StopServer extends ServerEvent {
  final Server server;

  StopServer(this.server);
}

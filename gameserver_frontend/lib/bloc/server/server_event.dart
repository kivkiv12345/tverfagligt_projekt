import 'package:gameserver_frontend/ServerListWidget.dart';
import 'package:gameserver_frontend/bloc/server/server_bloc.dart';

abstract class ServerEvent {}


class ServerStart extends ServerEvent {
  final ServerBloc server;

  ServerStart(this.server);
}

// class ServerStarted extends ServerEvent {
//   final ServerBloc server;

//   ServerStarted(this.server);
// }

// class ServerStopped extends ServerEvent {
//   final ServerBloc server;

//   ServerStopped(this.server);
// }

class ServerStop extends ServerEvent {
  final ServerBloc server;

  ServerStop(this.server);
}

// class ServerChanging extends ServerEvent {
//   final ServerBloc server;

//   ServerChanging(this.server);
// }

// class ServerError extends ServerEvent {
//   final ServerBloc server;

//   ServerError(this.server);
// }

import 'package:gameserver_frontend/ServerListWidget.dart';

abstract class ServerBlocState {
  final Server server;

  ServerBlocState(this.server);

  // ServerBlocState copyWith({
  //   Server? server,
  // }) {
  //   return this.class(
  //     server ?? this.server,
  //   );
  // }
}

class ServerRunningState extends ServerBlocState {
  ServerRunningState(super.server);
}

class ServerStoppedState extends ServerBlocState {
  ServerStoppedState(super.server);
}

class ServerChangingState extends ServerBlocState {
  ServerChangingState(super.server);
}

class ServerErrorState extends ServerBlocState {
  ServerErrorState(super.server);
}

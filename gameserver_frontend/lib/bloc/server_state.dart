import 'package:gameserver_frontend/ServerListWidget.dart';

enum ServerState { running, stopped, changing, error }

class ServerBlocState {
  ServerBlocState(this.state, this.statusCode);
  final ServerState state;
  final int statusCode;

  ServerBlocState copyWith({
    ServerState? state,
    int? statusCode,
  }) {
    return ServerBlocState(
      state ?? this.state,
      statusCode ?? this.statusCode,
    );
  }
}

class ServerUnloadedState extends ServerBlocState {
  ServerUnloadedState(super.state, super.statusCode);
}

class ServerLoadedBlocState extends ServerBlocState {
  ServerLoadedBlocState(this.servers, super.state, super.statusCode);

  final List<Server> servers;

  @override
  ServerLoadedBlocState copyWith({
    List<Server>? servers,
    ServerState? state,
    int? statusCode,
  }) {
    return ServerLoadedBlocState(
      servers ?? this.servers,
      state ?? this.state,
      statusCode ?? this.statusCode,
    );
  }
}

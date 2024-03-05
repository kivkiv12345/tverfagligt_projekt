
abstract class ServerBlocState {

  ServerBlocState();

  // ServerBlocState copyWith({
  //   Server? server,
  // }) {
  //   return this.class(
  //     server ?? this.server,
  //   );
  // }
}

class ServerRunningState extends ServerBlocState {
  ServerRunningState();
}

class ServerStoppedState extends ServerBlocState {
  ServerStoppedState();
}

class ServerChangingState extends ServerBlocState {
  ServerChangingState();
}

class ServerErrorState extends ServerBlocState {
  ServerErrorState();
}

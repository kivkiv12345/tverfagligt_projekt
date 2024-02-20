import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:gameserver_frontend/ServerListWidget.dart';
import 'package:gameserver_frontend/api.dart';
import 'package:gameserver_frontend/bloc/server_event.dart';
import 'package:gameserver_frontend/bloc/server_state.dart';

class ServerBloc extends Bloc<ServerEvent, ServerBlocState> {
  ServerBloc(ServerState state, int statusCode) : super(ServerUnloadedState(state, statusCode)) {
    on<StartServer>(startServer);
  }

  Future serverLoaded(ServerLoaded event, Emitter<ServerBlocState> emit) async {
    List<Server> serverlist = [];
    emit(ServerLoadedBlocState(serverlist, event.state, 100));
  }

  Future startServer(
    StartServer event,
    Emitter<ServerBlocState> emit,
  ) async {
    if (state is ServerLoadedBlocState) {
      final response = await event.server.start();
      ServerState _state;
      if (!bad_statuscode(response.statusCode)) {
        _state =
            ServerState.running; // Set state to running if start successful
      } else {
        _state =
            ServerState.stopped; // Set state back to stopped if start failed
      }
      emit(state.copyWith());
    }
  }

  @override
  Stream<ServerState> mapEventToState(ServerEvent event) async* {
    yield ServerState.changing; // Set state to changing while changing...

    if (event is StartServer) {
      final response = await event.server.start();

      if (!bad_statuscode(response.statusCode)) {
        yield ServerState.running; // Set state to running if start successful
      } else {
        yield ServerState.stopped; // Set state back to stopped if start failed
      }
    } else if (event is StopServer) {
      final response = await event.server.stop();

      if (!bad_statuscode(response.statusCode)) {
        yield ServerState.stopped; // Set state to stopped if stop successful
      } else {
        yield ServerState.running; // Set state back to running if stop failed
      }
    }
  }
}

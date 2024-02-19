import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:gameserver_frontend/api.dart';
import 'package:gameserver_frontend/bloc/server_event.dart';
import 'package:gameserver_frontend/bloc/server_state.dart';

class ServerBloc extends Bloc<ServerEvent, ServerState> {
  ServerBloc(super.state); // Initial state is stopped

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

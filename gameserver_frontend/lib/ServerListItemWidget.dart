import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:gameserver_frontend/ServerListWidget.dart';
import 'package:gameserver_frontend/bloc/server_bloc.dart';
import 'package:gameserver_frontend/bloc/server_event.dart';
import 'package:gameserver_frontend/bloc/server_state.dart';

class ServerListItemWidget extends StatelessWidget {
  final Server server;

  ServerListItemWidget({required this.server});

  @override
  Widget build(BuildContext context) {
    ServerBloc serverBloc = ServerBloc(this.server.state);  // Every server gets its own Bloc
    return BlocProvider(
      create: (context) => serverBloc,
      child: ListTile(
          title: Text(server.serverName),
          trailing: IconButton(
            icon: this._buildIconForState(server.state),
            onPressed: server.state is ServerChangingState
                ? null // Disable the button while the state is changing
                : () {
                    final ServerEvent event = server.state is ServerRunningState
                        ? ServerStop(server) // Create a StopServer event with the server object
                        : ServerStart(server); // Create a StartServer event with the server object
                    serverBloc.add(event); // Dispatch the event to the ServerBloc
                  },
          ),
        ),
    );
  }

  Widget _buildIconForState(ServerBlocState state) {
    if (state is ServerRunningState) {
      return const Icon(Icons.stop);
    } else if (state is ServerStoppedState) {
      return const Icon(Icons.play_arrow);
    } else if (state is ServerChangingState) {
      return CircularProgressIndicator();
    }
    return const Icon(Icons.error);
  }
}

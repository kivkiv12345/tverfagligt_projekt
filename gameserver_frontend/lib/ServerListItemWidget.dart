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
    return BlocListener<ServerBloc, ServerState>(
      listener: (context, state) {
        print("AAAAA");
        ScaffoldMessenger.of(context).showSnackBar(
              const SnackBar(content: Text('Server error occurred!')),
            );
        if (state is ServerError) {
            // Handle server error
            ScaffoldMessenger.of(context).showSnackBar(
              const SnackBar(content: Text('Server error occurred!')),
            );
          } else if (state is ServerChanging) {
            // Handle server changing state
            ScaffoldMessenger.of(context).showSnackBar(
              SnackBar(content: const Text('Server state is changing...')),
            );
          }
          // Add more conditions as needed
      },
      child: ListTile(
          title: Text(server.serverName),
          trailing: IconButton(
            icon: this._buildIconForState(server.state),
            onPressed: server.state == ServerState.changing
                ? null // Disable the button while the state is changing
                : () {
                    final ServerEvent event = server.state == ServerState.running
                        ? ServerStop(server) // Create a StopServer event with the server object
                        : ServerStart(server); // Create a StartServer event with the server object
                    // TODO Kevin: Can't find ServerBloc from context here!!
                    context.read<ServerBloc>().add(event); // Dispatch the event to the ServerBloc
                  },
          ),
        ),
    );
  }

  Widget _buildIconForState(ServerState state) {
    switch (state) {
      case ServerState.running:
        return const Icon(Icons.stop);
      case ServerState.stopped:
        return const Icon(Icons.play_arrow);
      case ServerState.changing:
        return CircularProgressIndicator();
      default:
        return const Icon(Icons.error);
    }
  }
}

import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:gameserver_frontend/api.dart';
import 'package:gameserver_frontend/bloc/server/server_bloc.dart';
import 'package:gameserver_frontend/bloc/server/server_event.dart';
import 'package:gameserver_frontend/bloc/server/server_state.dart';
import 'package:web_socket_channel/web_socket_channel.dart';

import 'dart:convert';

class ServerListItemWidget extends StatelessWidget {
  final ServerBloc server;

  ServerListItemWidget({required this.server}) {
    final wsUrl = Uri.parse('${Api.wsUrl}/server/${this.server.id}/');
    final channel = WebSocketChannel.connect(wsUrl);

    // NOTE: Constructor can't be async, but we don't really care to wait anyway,
    //  we only care to receive which can just happen whenever it's ready.
    //await channel.ready;

    channel.stream.listen((message) {
      // TODO Kevin: Ensure message enums are identical to backend by putting in library.
      String operation = json.decode(message)['message'];
      if (operation == 'Server opened') {
        this.server.add(ServerStarted(this.server));
      } else if (operation == 'Server closed') {
        this.server.add(ServerStopped(this.server));
      } else {
        print("Websocket received unknown message: $message");
      }
    });
  }

    @override
  Widget build(BuildContext context) {
    // Every server is its own Bloc
    return BlocBuilder(
      bloc: server,
      builder: (context, state) {
        return ListTile(
            title: Text(server.serverName),
            trailing: IconButton(
              icon: this._buildIconForState(this.server.state),
              onPressed: server.state is ServerChangingState
                  ? null // Disable the button while the state is changing
                  : () {
                      final ServerEvent event = server.state is ServerRunningState
                          ? ServerStop(server) // Create a StopServer event with the server object
                          : ServerStart(server); // Create a StartServer event with the server object
                      this.server.add(event); // Dispatch the event to the ServerBloc
                    },
            ),
          );
      }
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

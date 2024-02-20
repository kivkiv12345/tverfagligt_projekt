// Initially sourced from https://chat.openai.com

// Define Dart classes for JSON serialization
import 'package:dio/dio.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:gameserver_frontend/Exceptions.dart';
import 'package:gameserver_frontend/api.dart';
import 'package:gameserver_frontend/bloc/server_bloc.dart';
import 'package:gameserver_frontend/bloc/server_event.dart';
import 'package:gameserver_frontend/bloc/server_state.dart';


const String api_url = 'http://localhost:8000/api';

// Use Dio for HTTP requests
final dio = Dio();

class Server {
  final int id;
  final String serverName;
  final String game;
  final String serverVersion;
  final ServerState state;

  Server({
    required this.id,
    required this.serverName,
    required this.game,
    required this.serverVersion,
    required this.state,
  });

  // Add factory constructor to parse JSON
  factory Server.fromJson(Map<String, dynamic> json) {
    return Server(
      id: json['id'] as int,
      serverName: json['server_name'] as String,
      game: json['game'] as String,
      serverVersion: json['server_version'] as String,
      state: (json['is_running'] as bool) ? ServerState.running : ServerState.stopped, // Convert boolean to enum
    );
  }

  Future<Response> stop() async {
    final response = await dio.post('$api_url/stop-server/', data: {'server_ident': this.id});
    return response;
  }

  Future<Response> start() async {
    final response = await dio.post('$api_url/start-server/', data: {'server_ident': this.id});
    return response;
  }
}


class ServerListItem extends StatelessWidget {
  final Server server;

  ServerListItem({required this.server});

  @override
  Widget build(BuildContext context) {
    return ListTile(
      title: Text(server.serverName),
      trailing: IconButton(
        icon: server.state == ServerState.changing
            ? CircularProgressIndicator() // Display a loading indicator while the state is changing
            : server.state == ServerState.running
                ? Icon(Icons.stop)
                : Icon(Icons.play_arrow),
        onPressed: server.state == ServerState.changing
    ? null // Disable the button while the state is changing
    : () {
        final ServerEvent event = server.state == ServerState.running
            ? StopServer(server) // Create a StopServer event with the server object
            : StartServer(server); // Create a StartServer event with the server object
        context.read<ServerBloc>().add(event); // Dispatch the event to the ServerBloc
      },
      ),
    );
  }
}

// Widget to display list of servers
class ServersListWidget extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return BlocBuilder<ServerBloc, ServerBlocState>(
      builder: (context, state) {
        if (state.state == ServerState.changing) {
          return CircularProgressIndicator();
        } else if (state == ServerState.error) {
          return Text('Error');
        } else if (state is ServerLoadedBlocState) {
          final servers = state.servers;
          return ListView.builder(
            itemCount: servers.length,
            itemBuilder: (context, index) {
              final Server server = servers[index];
              return ListTile(
                title: Text(server.serverName),
                subtitle: Text(server.game),
                trailing: IconButton(
                  icon: Icon(server.state == ServerState.running ? Icons.stop : Icons.play_arrow),
                  onPressed: () {
                    context.read<ServerBloc>().add(server.state == ServerState.running ? StopServer(server) : StartServer(server));
                  },
                ),
              );
            },
          );
        }
        return Container(); // Placeholder widget
      },
    );
  }
}

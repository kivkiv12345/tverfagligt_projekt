// Initially sourced from https://chat.openai.com

// Define Dart classes for JSON serialization
import 'package:dio/dio.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:gameserver_frontend/Exceptions.dart';
import 'package:gameserver_frontend/ServerListItemWidget.dart';
import 'package:gameserver_frontend/api.dart';
import 'package:gameserver_frontend/bloc/server_bloc.dart';
import 'package:gameserver_frontend/bloc/server_event.dart';
import 'package:gameserver_frontend/bloc/server_state.dart';


class Server {
  final int id;
  final String serverName;
  final String game;
  final String serverVersion;
  final ServerBlocState state;

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

// Widget to display list of servers
class ServersListWidget extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return FutureBuilder<List<Server>>(
      future: fetchServers(),
      builder: (context, snapshot) {
        if (snapshot.connectionState == ConnectionState.waiting) {
          return CircularProgressIndicator();
        } else if (snapshot.hasError) {
          return Text('Error: ${snapshot.error}');
        } else if (!snapshot.hasData) {
          return Text('No data');
        }
    
        final servers = snapshot.data!;
        return ListView.builder(
          itemCount: servers.length,
          itemBuilder: (context, index) {
            final Server server = servers[index];
            return ServerListItemWidget(server: server,);
          }
        );
      },
    );
  }
}

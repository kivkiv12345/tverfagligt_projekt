// Initially sourced from https://chat.openai.com

// Define Dart classes for JSON serialization
import 'package:dio/dio.dart';
import 'package:flutter/material.dart';
import 'package:gameserver_frontend/Exceptions.dart';

// Define ServerBloc for state management
class ServerBloc {
  // Implement server-related state and actions
}

const String api_url = 'http://localhost:8000/api';

// Use Dio for HTTP requests
final dio = Dio();

class Server {
  final int id;
  final String serverName;
  final String game;
  final String serverVersion;
  final bool isRunning;

  Server({
    required this.id,
    required this.serverName,
    required this.game,
    required this.serverVersion,
    required this.isRunning,
  });

  // Add factory constructor to parse JSON
  factory Server.fromJson(Map<String, dynamic> json) {
    return Server(
      id: json['id'] as int,
      serverName: json['server_name'] as String,
      game: json['game'] as String,
      serverVersion: json['server_version'] as String,
      isRunning: json['is_running'] as bool,
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

bool bad_statuscode(int ?statusCode) {
  return statusCode == null || (statusCode < 200 || statusCode > 299);
}

// Fetch servers from backend
Future<List<Server>> fetchServers() async {
  // TODO Kevin: Set token during login
  dio.options.headers['Authorization'] = 'Token db35e66399468335c01b806c3c777fc4e4e9edb8';
  final response = await dio.get('$api_url/get-server-info');
  // Parse JSON response and return list of Server objects
  if (bad_statuscode(response.statusCode)) {
    throw ConnectionError('Failed to fetch servers');
  }

  final List<dynamic> jsonList = response.data as List<dynamic>;
  return jsonList.map((json) => Server.fromJson(json)).toList();
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
            return ListTile(
              title: Text(server.serverName),
              subtitle: Text(server.game),
              trailing: IconButton(
                icon: Icon(server.isRunning ? Icons.stop : Icons.play_arrow),
                onPressed: () async {
                  final Response response;
                  if (server.isRunning) {
                    response = await server.stop();
                  } else {
                    response = await server.start();
                  }

                  // TODO Kevin: Update widget... Bloc here??
                  // if (bad_statuscode(response.statusCode)) {
                  //  setState();  // TODO: Doesn't work, ServersListWidget is stateless
                  // }
                },
              ),
            );
          },
        );
      },
    );
  }
}

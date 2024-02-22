// Initially sourced from https://chat.openai.com

// Define Dart classes for JSON serialization
import 'package:dio/dio.dart';
import 'package:flutter/material.dart';
import 'package:gameserver_frontend/ServerListItemWidget.dart';
import 'package:gameserver_frontend/api.dart';
import 'package:gameserver_frontend/bloc/auth/user.dart';
import 'package:gameserver_frontend/bloc/server/server_bloc.dart';

// Widget to display list of servers
class ServersListWidget extends StatelessWidget {
  final AuthenticatedUser user;

  ServersListWidget(this.user);

  @override
  Widget build(BuildContext context) {
    return FutureBuilder<List<ServerBloc>>(
      future: this.user.api.fetchServers(),
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
            final ServerBloc server = servers[index];
            return ServerListItemWidget(server: server,);
          }
        );
      },
    );
  }
}

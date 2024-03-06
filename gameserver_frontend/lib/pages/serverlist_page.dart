import 'package:flutter/material.dart';
import 'package:gameserver_frontend/bloc/auth/user.dart';
import 'package:gameserver_frontend/widgets/server_list.dart';

class ServerListPage extends StatelessWidget {
  final AuthenticatedUser user;
  const ServerListPage(this.user);

  @override
  Widget build(BuildContext context) {
    return Center(child: ServersListWidget(this.user));
  }
}

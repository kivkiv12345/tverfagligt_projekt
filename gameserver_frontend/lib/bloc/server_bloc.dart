// ignore_for_file: unnecessary_this

import 'dart:async';

import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:gameserver_frontend/api.dart';
import 'package:gameserver_frontend/bloc/server_event.dart';
import 'package:gameserver_frontend/bloc/server_state.dart';

class ServerBloc extends Bloc<ServerEvent, ServerState> {
  ServerBloc(super.state) {
    on<ServerStart>(serverStart);
    on<ServerStarted>(serverStarted);
    on<ServerStop>(serverStop);
    on<ServerStopped>(serverStopped);
    on<ServerChanging>(serverChanging);
  }

  Future serverStart(ServerStart event, Emitter<ServerState> emit) async {
    this.add(ServerChanging(event.server));  // Should disable the server widget
    final response = await event.server.start();  // WebAPI call

    if (!bad_statuscode(response.statusCode)) {
      this.add(ServerStarted(event.server)); // Set state to started if start successful
    } else {
      this.add(ServerError(event.server)); // Something went wrong, now we don't know what's going on
    }

  }

  Future serverStarted(ServerStarted event, Emitter<ServerState> emit) async {
    // TODO Kevin: Enable server widget
  }

  Future serverStop(ServerStop event, Emitter<ServerState> emit) async {
    this.add(ServerChanging(event.server));  // Should disable the server widget
    final response = await event.server.stop();  // WebAPI call

    if (!bad_statuscode(response.statusCode)) {
      this.add(ServerStopped(event.server)); // Set state to stopped if stop successful
    } else {
      this.add(ServerError(event.server)); // Something went wrong, now we don't know what's going on
    }

  }

  Future serverStopped(ServerStopped event, Emitter<ServerState> emit) async {
    // TODO Kevin: Enable server widget
  }

  Future serverChanging(ServerChanging event, Emitter<ServerState> emit) async {

  }
}

// ignore_for_file: unnecessary_this

import 'dart:async';

import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:gameserver_frontend/api.dart';
import 'package:gameserver_frontend/bloc/server/server_event.dart';
import 'package:gameserver_frontend/bloc/server/server_state.dart';

class ServerBloc extends Bloc<ServerEvent, ServerBlocState> {
  final int id;
  final String serverName;
  final String game;
  final String serverVersion;

  ServerBloc(super.state, {
    required this.id,
    required this.serverName,
    required this.game,
    required this.serverVersion,
  }) {
    on<ServerStart>(serverStart);
    // on<ServerStarted>(serverStarted);
    on<ServerStop>(serverStop);
    // on<ServerStopped>(serverStopped);
    // on<ServerChanging>(serverChanging);
  }

  factory ServerBloc.fromJson(Map<String, dynamic> json) {
    return ServerBloc(
      (json['is_running'] as bool) ? ServerRunningState() : ServerStoppedState(), // Convert boolean to enum
      id: json['id'] as int,
      serverName: json['server_name'] as String,
      game: json['game'] as String,
      serverVersion: json['server_version'] as String,
    );
  }

  Future serverStart(ServerStart event, Emitter<ServerBlocState> emit) async {
    emit(ServerChangingState());  // Should disable the server widget

    final response = await dio.post('$api_url/start-server/', data: {'server_ident': this.id});  // WebAPI call

    if (!bad_statuscode(response.statusCode)) {
      emit(ServerRunningState());  // Set state to started if start successful
    } else {
      emit(ServerErrorState());  // Something went wrong, now we don't know what's going on
    }

  }

  // Future serverStarted(ServerStarted event, Emitter<ServerBlocState> emit) async {
  //   // TODO Kevin: Enable server widget
  //   emit(ServerRunningState());
  // }

  Future serverStop(ServerStop event, Emitter<ServerBlocState> emit) async {
    emit(ServerChangingState());  // Should disable the server widget

    final response = await dio.post('$api_url/stop-server/', data: {'server_ident': this.id});  // WebAPI call

    if (!bad_statuscode(response.statusCode)) {
      emit(ServerStoppedState()); // Set state to stopped if stop successful
    } else {
      emit(ServerErrorState()); // Something went wrong, now we don't know what's going on
    }

  }

  // Future serverStopped(ServerStopped event, Emitter<ServerBlocState> emit) async {
  //   // TODO Kevin: Enable server widget
  // }

  // Future serverChanging(ServerChanging event, Emitter<ServerBlocState> emit) async {

  // }
}

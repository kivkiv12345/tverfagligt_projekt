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
  final Api api;

  ServerBloc(super.state, {
    required this.id,
    required this.serverName,
    required this.game,
    required this.serverVersion,
    required this.api,
  }) {
    on<ServerStart>(serverStart);
    on<ServerStop>(serverStop);

    // These 2 are likely received from websockets.
    //  In any case, we don't question their validity.
    on<ServerStarted>(serverStarted);
    on<ServerStopped>(serverStopped);

    // on<ServerChanging>(serverChanging);
  }

  factory ServerBloc.fromJson(Map<String, dynamic> json, Api api) {
    return ServerBloc(
      (json['is_running'] as bool) ? ServerRunningState() : ServerStoppedState(), // Convert boolean to enum
      id: json['id'] as int,
      serverName: json['server_name'] as String,
      game: json['game'] as String,
      serverVersion: json['server_version'] as String,
      api: api,
    );
  }

  Future serverStart(ServerStart event, Emitter<ServerBlocState> emit) async {
    emit(ServerChangingState());  // Should disable the server widget

    final response = await this.api.dio.post('${this.api.api_url}/start-server/', data: {'server_ident': this.id});  // WebAPI call

    if (!bad_statuscode(response.statusCode)) {
      emit(ServerRunningState());  // Set state to started if start successful
    } else {
      emit(ServerErrorState());  // Something went wrong, now we don't know what's going on
    }

  }

  Future serverStarted(ServerStarted event, Emitter<ServerBlocState> emit) async {
    emit(ServerRunningState());
  }

  Future serverStop(ServerStop event, Emitter<ServerBlocState> emit) async {
    emit(ServerChangingState());  // Should disable the server widget

    final response = await this.api.dio.post('${this.api.api_url}/stop-server/', data: {'server_ident': this.id});  // WebAPI call

    if (!bad_statuscode(response.statusCode)) {
      emit(ServerStoppedState()); // Set state to stopped if stop successful
    } else {
      emit(ServerErrorState()); // Something went wrong, now we don't know what's going on
    }

  }

  Future serverStopped(ServerStopped event, Emitter<ServerBlocState> emit) async {
    emit(ServerStoppedState());
  }

  // Future serverChanging(ServerChanging event, Emitter<ServerBlocState> emit) async {

  // }
}

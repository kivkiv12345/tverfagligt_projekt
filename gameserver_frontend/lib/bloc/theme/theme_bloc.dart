


import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

class ThemeBloc extends Bloc<ThemeMode, ThemeMode> {

  ThemeBloc(super.initialState) {
    on<ThemeMode>(themeChange);
  }

  void themeChange(ThemeMode theme, Emitter<ThemeMode> emit) {
    emit(theme);
  }
}

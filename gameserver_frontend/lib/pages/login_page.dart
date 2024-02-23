// Mostly stolen from:
// https://github.com/TotallyNotRust/Chivalry-2-Competitive-Platform/blob/main/lib/pages/login_page.dart
import 'dart:io';

import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:gameserver_frontend/bloc/auth/auth_bloc.dart';
import 'package:gameserver_frontend/bloc/auth/auth_event.dart';

class LoginPage extends StatelessWidget {
  const LoginPage();

  @override
  Widget build(BuildContext context) {
    return const Center(child: LoginForm());
  }
}

class LoginForm extends StatelessWidget {
  const LoginForm();

  @override
  Widget build(BuildContext context) {
    double? width;
    if (Platform.isWindows || Platform.isLinux) {
      width = MediaQuery.of(context).size.width / 3;
    }

    TextEditingController usernameController = TextEditingController();
    TextEditingController passwordController = TextEditingController();

    return Container(
      color: Theme.of(context).scaffoldBackgroundColor,
      width: width,
      child: Padding(
        padding: const EdgeInsets.all(8.0),
        child: Column(
          children: [
            const Text("Username"),
            TextField(controller: usernameController),
            const Text("Password"),
            TextField(
              controller: passwordController,
              obscureText: true,
            ),
            CupertinoButton(
              child: const Text("Login"),
              onPressed: () async {
                BlocProvider.of<AuthBloc>(context)
                    .add(await LoginEvent.from_credentials(
                  usernameController.text,
                  passwordController.text,
                ));
              },
            )
          ],
        ),
      ),
    );
  }
}

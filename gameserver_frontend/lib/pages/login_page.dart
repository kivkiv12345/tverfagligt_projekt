// Mostly stolen from:
// https://github.com/TotallyNotRust/Chivalry-2-Competitive-Platform/blob/main/lib/pages/login_page.dart

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

    TextEditingController usernameController = TextEditingController();
    TextEditingController passwordController = TextEditingController();

    return Container(
      color: Theme.of(context).scaffoldBackgroundColor,
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
            MaterialButton(
              child: const Text("Login"),
              onPressed: () async {
                
                AuthEvent event = await LoginEvent.from_credentials(
                  usernameController.text,
                  passwordController.text,
                );

                if (event is LoginFailureEvent) {
                  ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(event.message)));
                }

                BlocProvider.of<AuthBloc>(context)
                    .add(event);
              },
            )
          ],
        ),
      ),
    );
  }
}

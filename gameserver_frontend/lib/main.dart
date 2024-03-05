import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:gameserver_frontend/ServerListWidget.dart';
import 'package:gameserver_frontend/bloc/auth/auth_bloc.dart';
import 'package:gameserver_frontend/bloc/auth/auth_event.dart';
import 'package:gameserver_frontend/bloc/auth/auth_state.dart';
import 'package:gameserver_frontend/bloc/auth/user.dart';
import 'package:gameserver_frontend/bloc/theme/theme_bloc.dart';
import 'package:gameserver_frontend/pages/login_page.dart';
import 'package:shared_preferences/shared_preferences.dart';



void main() {

  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return BlocProvider(
      create: (context) => ThemeBloc(
          ThemeMode.system), // Use system preferred dark/light mode by default.
      child: BlocBuilder<ThemeBloc, ThemeMode>(
        builder: (context, themeMode) {
          return MaterialApp(
            title: 'Flutter Demo',
            theme: ThemeData(
              colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
              useMaterial3: true,
            ),
            darkTheme: ThemeData.dark(),
            themeMode: themeMode,
            home: const MyHomePage(title: 'Flutter Demo Home Page'),
          );
        },
      ),
    );
  }
}

class MyHomePage extends StatefulWidget {
  const MyHomePage({super.key, required this.title});

  // This widget is the home page of your application. It is stateful, meaning
  // that it has a State object (defined below) that contains fields that affect
  // how it looks.

  // This class is the configuration for the state. It holds the values (in this
  // case the title) provided by the parent (in this case the App widget) and
  // used by the build method of the State. Fields in a Widget subclass are
  // always marked "final".

  final String title;

  @override
  State<MyHomePage> createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  @override
  Widget build(BuildContext context) {
    // This method is rerun every time setState is called, for instance as done
    // by the _incrementCounter method above.
    //
    // The Flutter framework has been optimized to make rerunning build methods
    // fast, so that you can just rebuild anything that needs updating rather
    // than having to individually change instances of widgets.
    return FutureBuilder<SharedPreferences>(
      future: () async {
        return await SharedPreferences.getInstance();
      }(),
      builder:
          (BuildContext context, AsyncSnapshot<SharedPreferences> snapshot) {
        if (!snapshot.hasData) {
          return CircularProgressIndicator();
        }

        SharedPreferences prefs = snapshot.data!;

        AuthBloc authBloc = AuthBloc.fromSharedPrefs(prefs);
        return BlocProvider(
          create: (context) => authBloc,
          child: BlocBuilder<AuthBloc, AuthBlocState>(
            bloc: authBloc,
            builder: (context, state) {
              final Widget content;

              if (state is LoggedInState) {
                AuthenticatedUser user = state.user;
                prefs.setString('token', user.api.token);
                prefs.setString('username', user.username);
                content = Center(
                  // Center is a layout widget. It takes a single child and positions it
                  // in the middle of the parent.
                  child: ServersListWidget(user),
                );
              } else {
                content = LoginPage();
              }

              return Scaffold(
                appBar: AppBar(
                  // TRY THIS: Try changing the color here to a specific color (to
                  // Colors.amber, perhaps?) and trigger a hot reload to see the AppBar
                  // change color while the other colors stay the same.
                  backgroundColor: Theme.of(context).colorScheme.inversePrimary,
                  // Here we take the value from the MyHomePage object that was created by
                  // the App.build method, and use it to set our appbar title.
                  title: Text(widget.title),
                  leading: Builder(
                    builder: (BuildContext context) {
                      return IconButton(
                        icon: Icon(Icons.menu),
                        onPressed: () {
                          Scaffold.of(context).openDrawer(); // Open the drawer
                        },
                      );
                    },
                  ),
                ),
                body: content,
                drawer: Drawer(
                  child: ListView(
                    padding: EdgeInsets.zero,
                    children: <Widget>[
                      DrawerHeader(
                        decoration: BoxDecoration(
                          color: Colors.blue,
                        ),
                        child: Text(
                          'Menu',
                          style: TextStyle(
                            color: Colors.white,
                            fontSize: 24,
                          ),
                        ),
                      ),
                      ListTile(
                        leading: Icon(Icons.settings),
                        title: Text('Settings'),
                        // onTap: () {
                        //   // Navigate to the settings page
                        //   Navigator.pop(context); // Close the drawer
                        //   Navigator.push(context,
                        //       MaterialPageRoute(builder: (context) => SettingsPage()));
                        // },
                      ),
                      if (state is LoggedInState)
                        Builder(builder: (context) {
                          return ListTile(
                            leading: Icon(Icons.logout),
                            title: Text('Log Out'),
                            onTap: () {
                              prefs.remove('username');
                              prefs.remove('token');
                              BlocProvider.of<AuthBloc>(context)
                                  .add(LogoutEvent(user: state.user));
                              Scaffold.of(context).closeDrawer();
                            },
                          );
                        }),
                      ListTile(
                        title: Text('Dark Mode'),
                        trailing: Switch(
                          value:
                              Theme.of(context).brightness == Brightness.dark,
                          onChanged: (value) {
                            // Toggle dark mode
                            ThemeMode newThemeMode =
                                value ? ThemeMode.dark : ThemeMode.light;
                            MediaQuery.platformBrightnessOf(context);
                            var newBrightness =
                                MediaQuery.of(context).platformBrightness;
                            if (newBrightness == Brightness.dark) {
                              ThemeMode.dark;
                            }
                            BlocProvider.of<ThemeBloc>(context).add(newThemeMode);
                          },
                        ),
                      ),
                    ],
                  ),
                ),
              );
            },
          ),
        );
      },
    );
  }
}

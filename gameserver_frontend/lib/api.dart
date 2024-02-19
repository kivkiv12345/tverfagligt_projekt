import 'package:gameserver_frontend/Exceptions.dart';
import 'package:gameserver_frontend/ServerListWidget.dart';
import 'package:gameserver_frontend/bloc/server_event.dart';

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

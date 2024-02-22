import 'package:dio/dio.dart';
import 'package:gameserver_frontend/Exceptions.dart';
import 'package:gameserver_frontend/ServerListWidget.dart';
import 'package:gameserver_frontend/bloc/server/server_bloc.dart';
import 'package:gameserver_frontend/bloc/server/server_event.dart';


bool bad_statuscode(int ?statusCode) {
  return statusCode == null || (statusCode < 200 || statusCode > 299);
}

class Api {
  
  static const String url = 'http://localhost:8000/api'; 
  late final Dio _dio;  // Use Dio for HTTP requests

  // late final String token;  // TODO Kevin: What if token changes?

  Api(String token) {
    this._dio = Dio();
    this._dio.options.headers['Authorization'] = 'Token $token';
  }

  Api._with_dio(String token, Dio dio) {
    this._dio = dio;
    this._dio.options.headers['Authorization'] = 'Token $token';
  }

  static Future<Api> from_credentials(String username, String password) async {
    Dio dio = Dio();
    String cred_str = '{"username": $username, "password": $password}';  // TODO Kevin: What if token changes?
    Response response = await dio.post(Api.url, data: cred_str);
    String token = response.data as String;
    return Api._with_dio(token, dio);
  }
  
  // String fetchToken() {
  //   return 
  // }

  // Fetch servers from backend
  Future<List<ServerBloc>> fetchServers() async {
    // TODO Kevin: Set token during login
    final response = await this._dio.get('${Api.url}/get-server-info');
    // Parse JSON response and return list of Server objects
    if (bad_statuscode(response.statusCode)) {
      throw ConnectionError('Failed to fetch servers');
    }

    final List<dynamic> jsonList = response.data as List<dynamic>;
    return jsonList.map((json) => ServerBloc.fromJson(json)).toList();
  }
}
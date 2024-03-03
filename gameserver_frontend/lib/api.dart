import 'package:dio/dio.dart';
import 'package:gameserver_frontend/Exceptions.dart';
import 'package:gameserver_frontend/bloc/server/server_bloc.dart';


bool bad_statuscode(int ?statusCode) {
  return statusCode == null || (statusCode < 200 || statusCode > 299);
}

class Api {
  
  static const String wsUrl = 'ws://127.0.0.1:8000/ws';
  static const String url = 'http://localhost:8000/api';
  final String api_url = Api.url;
  late final Dio dio;  // Use Dio for HTTP requests
  final String token;

  // late final String token;  // TODO Kevin: What if token changes?

  static Dio _get_base_dio() {
    return Dio(BaseOptions(
      // followRedirects: false,  // Seems to be recommended, but breaks get-server-info, which is apparently 'moved permanently'
      validateStatus: (status) {
        return status! < 500;
      },
    ));
  }

  Api(this.token) {
    this.dio = Api._get_base_dio();
    this.dio.options.headers['Authorization'] = 'Token ${this.token}';
  }

  Api._with_dio(this.token, Dio dio) {
    this.dio = dio;
    this.dio.options.headers['Authorization'] = 'Token ${this.token}';
  }

  Future<Response> logout() async {
    return await await this.dio.post('${Api.url}/user-logout/');  // WebAPI call
  }

  static Future<Api> from_credentials(String username, String password) async {
    Dio dio = Api._get_base_dio();
    String cred_str = '{"username": "$username", "password": "$password"}';  // TODO Kevin: What if token changes?
    Response response = await dio.post('${Api.url}/user-login/', data: cred_str);  // TODO Kevin: Exception if server is down

    if (bad_statuscode(response.statusCode)) {
      throw PermissionDeniedError("Login failed, ${response.data}");
    }

    String token = (response.data as Map<String, dynamic>)['token']!;
    return Api._with_dio(token, dio);
  }
  
  // String fetchToken() {
  //   return 
  // }

  // Fetch servers from backend
  Future<List<ServerBloc>> fetchServers() async {
    // TODO Kevin: Set token during login
    final response = await this.dio.get('${Api.url}/get-server-info');
    // Parse JSON response and return list of Server objects
    if (bad_statuscode(response.statusCode)) {
      throw ConnectionError('Failed to fetch servers');
    }

    final List<dynamic> jsonList = response.data as List<dynamic>;
    return jsonList.map((json) => ServerBloc.fromJson(json, this)).toList();
  }
}

import 'package:http/http.dart' as http;
import 'dart:convert';

class ApiService {
  final String _baseUrl = 'http://localhost:8000/api/v1';

  Future<String> getChatbotResponse(String message) async {
    final response = await http.post(
      Uri.parse('$_baseUrl/chat/message'),
      headers: {'Content-Type': 'application/json'},
      body: json.encode({'message': message}),
    );

    if (response.statusCode == 200) {
      return json.decode(response.body)['response'];
    } else {
      throw Exception('Failed to get chatbot response');
    }
  }
}

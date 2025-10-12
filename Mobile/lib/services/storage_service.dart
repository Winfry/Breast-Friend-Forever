
import 'package:shared_preferences/shared_preferences.dart';

class StorageService {
  Future<void> saveUserName(String userName) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString('userName', userName);
  }

  Future<String?> getUserName() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getString('userName');
  }
}

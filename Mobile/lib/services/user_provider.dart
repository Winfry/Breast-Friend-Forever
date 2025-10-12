
import 'package:flutter/foundation.dart';

class UserProvider with ChangeNotifier {
  String _userName = 'Friend';

  String get userName => _userName;

  void setUserName(String name) {
    _userName = name;
    notifyListeners();
  }
}

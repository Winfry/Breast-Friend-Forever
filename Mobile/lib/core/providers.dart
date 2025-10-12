import 'package:provider/provider.dart';
import 'package:breast_friend_flutter/services/app_provider.dart';
import 'package:breast_friend_flutter/services/user_provider.dart';
import 'package:breast_friend_flutter/services/progress_provider.dart';

class AppProviders {
  static List<ChangeNotifierProvider> get providers {
    return [
      ChangeNotifierProvider(create: (_) => AppProvider()),
      ChangeNotifierProvider(create: (_) => UserProvider()),
      ChangeNotifierProvider(create: (_) => ProgressProvider()),
    ];
  }
}
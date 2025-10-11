import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../services/app_provider.dart';
import '../services/user_provider.dart';
import '../services/progress_provider.dart';

class AppProviders {
  static List<ChangeNotifierProvider> get providers {
    return [
      ChangeNotifierProvider(create: (_) => AppProvider()),
      ChangeNotifierProvider(create: (_) => UserProvider()),
      ChangeNotifierProvider(create: (_) => ProgressProvider()),
    ];
  }
}
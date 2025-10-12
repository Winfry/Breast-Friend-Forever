import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'core/providers.dart';
import 'app.dart';

void main() {
  runApp(
    MultiProvider(
      providers: AppProviders.providers,
      child: const BreastFriendApp(),
    ),
  );
}
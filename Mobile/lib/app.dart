
import 'package:flutter/material.dart';
import 'package:breast_friend_flutter/screens/chat_screen.dart';
import 'package:breast_friend_flutter/screens/encouragement_screen.dart';
import 'package:breast_friend_flutter/screens/home_screen.dart';
import 'package:breast_friend_flutter/screens/hospitals_screen.dart';
import 'package:breast_friend_flutter/screens/resources_screen.dart';
import 'package:breast_friend_flutter/screens/self_exam_screen.dart';
import 'package:breast_friend_flutter/core/app_theme.dart';

class BreastFriendApp extends StatelessWidget {
  const BreastFriendApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Breast Friend Forever',
      theme: AppTheme.lightTheme,
      initialRoute: '/',
      routes: {
        '/': (context) => const HomeScreen(),
        '/self-exam': (context) => const SelfExamScreen(),
        '/chat': (context) => const ChatScreen(),
        '/resources': (context) => const ResourcesScreen(),
        '/screening': (context) => const HospitalsScreen(),
        '/community': (context) => const EncouragementScreen(),
      },
    );
  }
}

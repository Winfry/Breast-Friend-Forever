import 'package:flutter/material.dart';
import '../screens/home_screen.dart';
import '../screens/self_exam_screen.dart';
import '../screens/chat_screen.dart';
import '../screens/resources_screen.dart';
import '../screens/screening_screen.dart';
import '../screens/community_screen.dart';

class AppRoutes {
  static const String home = '/';
  static const String selfExam = '/self-exam';
  static const String chat = '/chat';
  static const String resources = '/resources';
  static const String screening = '/screening';
  static const String community = '/community';

  static Map<String, WidgetBuilder> get routes {
    return {
      home: (context) => const HomeScreen(),
      selfExam: (context) => const SelfExamScreen(),
      chat: (context) => const ChatScreen(),
      resources: (context) => const ResourcesScreen(),
      screening: (context) => const ScreeningScreen(),
      community: (context) => const CommunityScreen(),
    };
  }
}
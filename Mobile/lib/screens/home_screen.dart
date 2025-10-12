import 'package:flutter/material.dart';
import 'package:lottie/lottie.dart';
import 'package:breast_friend_flutter/widgets/feature_card.dart';
import 'package:breast_friend_flutter/widgets/stats_card.dart';
import '../core/app_theme.dart';

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final features = [
      {
        'title': '🤗 Self-Exam Guide',
        'description': 'Step-by-step guidance with love and care',
        'color': AppTheme.primaryColor,
        'route': '/self-exam',
        'animation': 'assets/animations/heart.json',
      },
      {
        'title': '💬 Chat Assistant',
        'description': 'Ask anything, no judgment',
        'color': AppTheme.secondaryColor,
        'route': '/chat',
        'animation': 'assets/animations/chat.json',
      },
      {
        'title': '📚 Resources',
        'description': 'Learn at your own pace',
        'color': const Color(0xFFDB2777),
        'route': '/resources',
        'animation': 'assets/animations/book.json',
      },
      {
        'title': '🏥 Find Screening',
        'description': 'Locate caring professionals near you',
        'color': const Color(0xFFBE185D),
        'route': '/screening',
        'animation': 'assets/animations/location.json',
      },
      {
        'title': '💕 Encouragement Wall',
        'description': 'Share hope and strength',
        'color': const Color(0xFF9D174D),
        'route': '/community',
        'animation': 'assets/animations/community.json',
      },
    ];

    return Scaffold(
      backgroundColor: AppTheme.lightTheme.scaffoldBackgroundColor,
      body: SafeArea(
        child: SingleChildScrollView(
          child: Column(
            children: [
              // Header Section
              Container(
                width: double.infinity,
                padding: const EdgeInsets.all(30),
                decoration: BoxDecoration(
                  gradient: const LinearGradient(
                    colors: [
                      Color(0xFFFF69B4),
                      Color(0xFFFF1493),
                      Color(0xFFDB2777),
                    ],
                    begin: Alignment.topLeft,
                    end: Alignment.bottomRight,
                  ),
                  borderRadius: const BorderRadius.only(
                    bottomLeft: Radius.circular(30),
                    bottomRight: Radius.circular(30),
                  ),
                  boxShadow: [
                    BoxShadow(
                      color: Colors.pink.withAlpha((255 * 0.3).round()),
                      blurRadius: 20,
                      offset: const Offset(0, 10),
                    ),
                  ],
                ),
                child: Column(
                  children: [
                    Text(
                      '💖 Breast Friend Forever',
                      style: Theme.of(context).textTheme.displayLarge?.copyWith(
                            color: Colors.white,
                            fontSize: 28,
                          ),
                      textAlign: TextAlign.center,
                    ),
                    const SizedBox(height: 8),
                    Text(
                      'Your compassionate breast health companion',
                      style: Theme.of(context).textTheme.bodyLarge?.copyWith(
                            color: Colors.white.withAlpha((255 * 0.9).round()),
                            fontSize: 16,
                          ),
                      textAlign: TextAlign.center,
                    ),
                  ],
                ),
              ),

              // Welcome Animation
              Container(
                margin: const EdgeInsets.all(20),
                padding: const EdgeInsets.all(20),
                decoration: BoxDecoration(
                  color: Colors.white,
                  borderRadius: BorderRadius.circular(20),
                  boxShadow: [
                    BoxShadow(
                      color: Colors.black.withAlpha((255 * 0.1).round()),
                      blurRadius: 10,
                      offset: const Offset(0, 4),
                    ),
                  ],
                ),
                child: Column(
                  children: [
                    Lottie.asset(
                      'assets/animations/welcome.json',
                      height: 150,
                      fit: BoxFit.contain,
                    ),
                    const SizedBox(height: 10),
                    Text(
                      'Welcome, Beautiful Soul! We\'re so glad you\'re here. 🌸',
                      style: Theme.of(context).textTheme.bodyLarge?.copyWith(
                            color: Colors.black54,
                          ),
                      textAlign: TextAlign.center,
                    ),
                  ],
                ),
              ),

              // Features Section
              Padding(
                padding: const EdgeInsets.all(20),
                child: Text(
                  'How Can We Support You Today?',
                  style: Theme.of(context).textTheme.displayMedium?.copyWith(
                        color: AppTheme.primaryColor,
                      ),
                  textAlign: TextAlign.center,
                ),
              ),

              // Features Grid
              ...features.map((feature) => FeatureCard(
                    title: feature['title'] as String,
                    description: feature['description'] as String,
                    color: feature['color'] as Color,
                    animationPath: feature['animation'] as String,
                    onTap: () {
                      Navigator.pushNamed(context, feature['route'] as String);
                    },
                  )),

              // Statistics Section
              Container(
                margin: const EdgeInsets.all(20),
                padding: const EdgeInsets.all(20),
                decoration: BoxDecoration(
                  color: Colors.white,
                  borderRadius: BorderRadius.circular(20),
                  boxShadow: [
                    BoxShadow(
                      color: Colors.black.withAlpha((255 * 0.1).round()),
                      blurRadius: 10,
                      offset: const Offset(0, 4),
                    ),
                  ],
                ),
                child: Column(
                  children: [
                    Text(
                      'Our Community Impact',
                      style: Theme.of(context).textTheme.displayMedium?.copyWith(
                            color: AppTheme.primaryColor,
                          ),
                      textAlign: TextAlign.center,
                    ),
                    const SizedBox(height: 20),
                    const Row(
                      children: [
                        Expanded(
                          child: StatsCard(
                            number: '1,234+',
                            label: 'Lives Touched',
                            emoji: '💖',
                          ),
                        ),
                        Expanded(
                          child: StatsCard(
                            number: '567+',
                            label: 'Self-Exams Guided',
                            emoji: '🖐️',
                          ),
                        ),
                      ],
                    ),
                    const SizedBox(height: 10),
                    const Row(
                      children: [
                        Expanded(
                          child: StatsCard(
                            number: '89+',
                            label: 'Questions Answered',
                            emoji: '💬',
                          ),
                        ),
                        Expanded(
                          child: StatsCard(
                            number: '100%',
                            label: 'Love & Support',
                            emoji: '🌈',
                          ),
                        ),
                      ],
                    ),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
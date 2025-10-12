import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:breast_friend_flutter/services/progress_provider.dart';
import 'package:breast_friend_flutter/widgets/step_card.dart';

class SelfExamScreen extends StatefulWidget {
  const SelfExamScreen({super.key});

  @override
  State<SelfExamScreen> createState() => _SelfExamScreenState();
}

class _SelfExamScreenState extends State<SelfExamScreen> {
  int _currentStep = 1;

  final List<Map<String, dynamic>> _examSteps = [
    {
      'id': 1,
      'title': 'Get Comfortable & Relax',
      'description': 'Find a quiet, private space where you can relax. Sit or stand in front of a mirror with your shoulders straight and arms on your hips.',
      'animation': 'assets/animations/mirror-check.json',
      'tip': '💖 Be gentle with yourself - this is about loving awareness, not criticism',
      'tipColor': Color(0xFFFF69B4),
    },
    {
      'id': 2,
      'title': 'Visual Inspection',
      'description': 'Look for any changes in size, shape, color, or visible distortion. Check for swelling, dimpling, puckering, or changes in the nipple.',
      'animation': 'assets/animations/arms-up.json',
      'tip': '🌈 You\'re building a powerful health habit - that\'s something to celebrate!',
      'tipColor': Color(0xFFEC4899),
    },
    {
      'id': 3,
      'title': 'Raise Arms & Inspect',
      'description': 'Raise your arms overhead and look for the same changes. Notice if there\'s any fluid coming from one or both nipples.',
      'animation': 'assets/animations/arms-up.json',
      'tip': '🎵 Put on some calming music - make this your special self-care time',
      'tipColor': Color(0xFFDB2777),
    },
    {
      'id': 4,
      'title': 'Lie Down & Feel',
      'description': 'Lie down and use your right hand to feel your left breast, then left hand for right breast. Use a firm, smooth touch with the first few finger pads.',
      'animation': 'assets/animations/lie-down.json',
      'tip': '💫 You\'re learning your body\'s unique landscape - how amazing is that!',
      'tipColor': Color(0xFFBE185D),
    },
    {
      'id': 5,
      'title': 'Follow a Pattern',
      'description': 'Use a systematic pattern - circular, up-and-down, or wedge. Cover the entire breast from collarbone to top of abdomen, armpit to cleavage.',
      'animation': 'assets/animations/circular-motion.json',
      'tip': '🌟 Consistency creates confidence - you\'re building a lifelong health skill',
      'tipColor': Color(0xFF9D174D),
    },
    {
      'id': 6,
      'title': 'Final Check Standing/Sitting',
      'description': 'Many women find it easiest to feel their breasts when skin is wet, so this step can be done in the shower. Repeat the same hand movements.',
      'animation': 'assets/animations/shower-check.json',
      'tip': '🎉 You did it! Regular checks are a beautiful act of self-love and care',
      'tipColor': Color(0xFF831843),
    },
  ];

  void _completeStep(int stepId) {
    final progressProvider = Provider.of<ProgressProvider>(context, listen: false);
    progressProvider.completeExamStep(stepId);
    
    if (_currentStep < _examSteps.length) {
      setState(() {
        _currentStep++;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    final progressProvider = Provider.of<ProgressProvider>(context);
    final completedSteps = progressProvider.completedExamSteps;
    final progress = _currentStep / _examSteps.length;

    return Scaffold(
      appBar: AppBar(
        title: const Text('🤗 Self-Exam Guide'),
        backgroundColor: Theme.of(context).primaryColor,
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            // Progress Tracker
            Container(
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
                                  ],              ),
              child: Column(
                children: [
                  Text(
                    'Your Self-Exam Journey',
                    style: Theme.of(context).textTheme.displayMedium?.copyWith(
                          color: Theme.of(context).primaryColor,
                        ),
                  ),
                  const SizedBox(height: 16),
                  LinearProgressIndicator(
                    value: progress,
                    backgroundColor: Colors.grey[200],
                    valueColor: AlwaysStoppedAnimation<Color>(
                      Theme.of(context).primaryColor,
                    ),
                    borderRadius: BorderRadius.circular(10),
                    minHeight: 12,
                  ),
                  const SizedBox(height: 8),
                  Text(
                    'Step $_currentStep of ${_examSteps.length} completed',
                    style: Theme.of(context).textTheme.bodyMedium,
                  ),
                ],
              ),
            ),

            const SizedBox(height: 20),

            // Current Step
            ..._examSteps.where((step) => step['id'] == _currentStep).map(
                  (step) => StepCard(
                    stepNumber: step['id'],
                    title: step['title'],
                    description: step['description'],
                    animationPath: step['animation'],
                    tip: step['tip'],
                    tipColor: step['tipColor'],
                    isCompleted: completedSteps.contains(step['id']),
                    onComplete: () => _completeStep(step['id']),
                    onPractice: () {
                      // Practice mode implementation
                      ScaffoldMessenger.of(context).showSnackBar(
                        SnackBar(
                          content: Text('Practicing: ${step['title']}'),
                          backgroundColor: Theme.of(context).primaryColor,
                        ),
                      );
                    },
                  ),
                ),
          ],
        ),
      ),
    );
  }
}
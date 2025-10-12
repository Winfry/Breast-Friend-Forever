
import 'package:flutter/material.dart';
import 'package:lottie/lottie.dart';

class StepCard extends StatelessWidget {
  final int stepNumber;
  final String title;
  final String description;
  final String animationPath;
  final String tip;
  final Color tipColor;
  final bool isCompleted;
  final VoidCallback onComplete;
  final VoidCallback onPractice;

  const StepCard({
    super.key,
    required this.stepNumber,
    required this.title,
    required this.description,
    required this.animationPath,
    required this.tip,
    required this.tipColor,
    required this.isCompleted,
    required this.onComplete,
    required this.onPractice,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      elevation: 4,
      margin: const EdgeInsets.symmetric(vertical: 10),
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(15),
      ),
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text('Step $stepNumber: $title', style: Theme.of(context).textTheme.headline6),
            const SizedBox(height: 10),
            Text(description, style: Theme.of(context).textTheme.bodyText2),
            const SizedBox(height: 10),
            Lottie.asset(animationPath, height: 150),
            const SizedBox(height: 10),
            Container(
              padding: const EdgeInsets.all(12),
              decoration: BoxDecoration(
                color: tipColor.withOpacity(0.2),
                borderRadius: BorderRadius.circular(10),
              ),
              child: Text(tip, style: TextStyle(color: tipColor, fontStyle: FontStyle.italic)),
            ),
            const SizedBox(height: 10),
            Row(
              mainAxisAlignment: MainAxisAlignment.end,
              children: [
                TextButton(onPressed: onPractice, child: const Text('Practice')),
                const SizedBox(width: 10),
                ElevatedButton(
                  onPressed: onComplete,
                  style: ElevatedButton.styleFrom(
                    backgroundColor: isCompleted ? Colors.green : Theme.of(context).primaryColor,
                  ),
                  child: Text(isCompleted ? 'Completed' : 'Mark as Complete'),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}

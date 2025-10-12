
import 'package:flutter/material.dart';

class StatsCard extends StatelessWidget {
  final String number;
  final String label;
  final String emoji;

  const StatsCard({
    super.key,
    required this.number,
    required this.label,
    required this.emoji,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      elevation: 2,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(15),
      ),
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            Text(emoji, style: const TextStyle(fontSize: 24)),
            const SizedBox(height: 8),
            Text(number, style: Theme.of(context).textTheme.headlineSmall),
            const SizedBox(height: 4),
            Text(label, style: Theme.of(context).textTheme.bodyMedium, textAlign: TextAlign.center),
          ],
        ),
      ),
    );
  }
}


import 'package:flutter/material.dart';
import 'package:breast_friend_flutter/models/hospital.dart';

class HospitalCard extends StatelessWidget {
  final Hospital hospital;

  const HospitalCard({super.key, required this.hospital});

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
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(hospital.name, style: Theme.of(context).textTheme.headlineSmall),
            const SizedBox(height: 8),
            Text(hospital.address, style: Theme.of(context).textTheme.bodyMedium),
            const SizedBox(height: 8),
            Row(
              children: [
                const Icon(Icons.star, color: Colors.amber, size: 16),
                const SizedBox(width: 4),
                Text(hospital.rating.toString(), style: Theme.of(context).textTheme.bodyMedium),
              ],
            ),
          ],
        ),
      ),
    );
  }
}

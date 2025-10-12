
import 'package:flutter/material.dart';
import 'package:breast_friend_flutter/models/resource.dart';
import 'package:url_launcher/url_launcher.dart';

class ResourceCard extends StatelessWidget {
  final Resource resource;

  const ResourceCard({super.key, required this.resource});

  @override
  Widget build(BuildContext context) {
    return Card(
      elevation: 2,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(15),
      ),
      child: InkWell(
        onTap: () async {
          if (await canLaunchUrl(Uri.parse(resource.url))) {
            await launchUrl(Uri.parse(resource.url));
          } else {
            throw 'Could not launch ${resource.url}';
          }
        },
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(resource.title, style: Theme.of(context).textTheme.headlineSmall),
              const SizedBox(height: 8),
              Text(resource.description, style: Theme.of(context).textTheme.bodyMedium),
            ],
          ),
        ),
      ),
    );
  }
}

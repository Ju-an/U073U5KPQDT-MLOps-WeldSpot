import 'dart:io';
import 'package:flutter/material.dart';
import 'package:firebase_storage/firebase_storage.dart';
import 'package:path/path.dart';

class FeedbackPopup extends StatefulWidget {
  final String imagePath;
  final Map<String, double> classification;

  FeedbackPopup({required this.imagePath, required this.classification});

  @override
  _FeedbackPopupState createState() => _FeedbackPopupState();
}

class _FeedbackPopupState extends State<FeedbackPopup> {
  final List<String> categories = [
    'Background',
    'Bad Welding',
    'Crack',
    'Excess Reinforcement',
    'Good Welding',
    'Porosity',
    'Splatters'
  ];

  final Map<String, bool> selectedCategories = {};

  @override
  void initState() {
    super.initState();
    for (var category in categories) {
      selectedCategories[category] = false;
    }
  }

  Future<void> sendFeedback() async {
    final timestamp = DateTime.now().millisecondsSinceEpoch;
    final feedbackString = widget.classification.entries.map((entry) {
      final category = entry.key;
      final value = entry.value;
      final selected = selectedCategories[category]!;
      return '${selected ? 1 : 0}-${value.toStringAsFixed(1)}';
    }).join('_');
    final fileName = '$timestamp_$feedbackString.jpg';
    final file = File(widget.imagePath);

    try {
      await FirebaseStorage.instance.ref('feedback/$fileName').putFile(file);
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Feedback sent successfully')));
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Error sending feedback: $e')));
    }
    Navigator.of(context).pop();
  }

  @override
  Widget build(BuildContext context) {
    return AlertDialog(
      title: Text('Send Feedback'),
      content: SingleChildScrollView(
        child: ListBody(
          children: categories.map((category) {
            return CheckboxListTile(
              title: Text(category),
              value: selectedCategories[category],
              onChanged: (bool? value) {
                setState(() {
                  selectedCategories[category] = value!;
                });
              },
            );
          }).toList(),
        ),
      ),
      actions: [
        TextButton(
          onPressed: sendFeedback,
          child: Text('Send Feedback'),
        ),
      ],
    );
  }
}

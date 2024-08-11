import 'dart:convert';
import 'dart:developer';
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

  Future<void> sendFeedback(BuildContext context) async {
    final timestamp = DateTime.now().millisecondsSinceEpoch;
    log("selectedCategories: $selectedCategories");
    final List<String> keys = selectedCategories.keys.toList();
    final List<bool> values =
        keys.map((key) => selectedCategories[key]!).toList();
    final feedbackString = widget.classification.entries.map((entry) {
      log("entry: ${entry.key} - ${entry.value}");
      final category =
          entry.key.replaceAll('\r', '').replaceAll('\n', '').trim();
      final value = entry.value;
      bool selected = false;
      int index = -1;
      for (int i = 0; i < categories.length; i++) {
        if (categories[i] == category) {
          index = i;
          break;
        }
      }
      if (index != -1) {
        selected = values[index];
        log('Selected $category: $selected');
      } else {
        log('Category $category not found in $values');
      }
      return '${selected ? 1 : 0}-${value.toStringAsFixed(1)}';
    }).join('_');
    final fileName = '${timestamp}_$feedbackString.jpg';
    final file = File(widget.imagePath);
    log("Sending feedback to Firebase: $fileName");
    try {
      await FirebaseStorage.instance.ref('$fileName').putFile(file);
      ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Feedback sent successfully')));
    } catch (e) {
      ScaffoldMessenger.of(context)
          .showSnackBar(SnackBar(content: Text('Error sending feedback: $e')));
    }
    Navigator.of(context).pop();
  }

  @override
  Widget build(BuildContext context) {
    return AlertDialog(
      title: const Text('Send Feedback'),
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
          onPressed: () => sendFeedback(context),
          child: const Text('Send Feedback'),
        ),
      ],
    );
  }
}

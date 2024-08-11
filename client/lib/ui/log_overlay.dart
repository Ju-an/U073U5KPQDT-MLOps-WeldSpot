import 'package:flutter/material.dart';

class LogOverlay extends StatefulWidget {
  const LogOverlay({Key? key}) : super(key: key);

  @override
  _LogOverlayState createState() => _LogOverlayState();
}

class _LogOverlayState extends State<LogOverlay> {
  final List<String> _logs = [];

  void addLog(String message) {
    setState(() {
      if (_logs.length >= 5) {
        _logs.removeAt(0);
      }
      _logs.add(message);
    });
  }

  @override
  Widget build(BuildContext context) {
    return Positioned(
      top: 0,
      left: 0,
      right: 0,
      child: Container(
        color: Colors.black.withOpacity(0.5),
        padding: const EdgeInsets.all(8.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: _logs.map((log) => Text(log, style: TextStyle(color: Colors.white))).toList(),
        ),
      ),
    );
  }
}

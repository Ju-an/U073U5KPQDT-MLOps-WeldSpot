/*
 * Copyright 2023 The TensorFlow Authors. All Rights Reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *             http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

import 'dart:io';
import 'package:camera/camera.dart';
import 'package:flutter/material.dart';
import 'package:image_classification_mobilenet/helper/image_classification_helper.dart';

class CameraScreen extends StatefulWidget {
  const CameraScreen({
    super.key,
    required this.camera,
  });

  final CameraDescription camera;

  @override
  State<StatefulWidget> createState() => CameraScreenState();
}

class CameraScreenState extends State<CameraScreen>
    with WidgetsBindingObserver {
  late CameraController cameraController;
  late ImageClassificationHelper imageClassificationHelper;
  Map<String, double>? classification;
  bool _isProcessing = false;
  double? _fps;
  double _confidenceThreshold = 0.5;

  // init camera
  initCamera() {
    cameraController = CameraController(widget.camera, ResolutionPreset.medium,
        imageFormatGroup: Platform.isIOS
            ? ImageFormatGroup.bgra8888
            : ImageFormatGroup.yuv420);
    cameraController.initialize().then((value) {
      cameraController.startImageStream(imageAnalysis);
      if (mounted) {
        setState(() {});
      }
    });
  }

  Future<void> imageAnalysis(CameraImage cameraImage) async {
    // if image is still analyze, skip this frame
    if (_isProcessing) {
      return;
    }
    _isProcessing = true;

    final startTime = DateTime.now();
    classification =
        await imageClassificationHelper.inferenceCameraFrame(cameraImage);
    // Filter based on confidence threshold and "Background" class.
    if (classification != null) {
      var entries = classification!.entries.toList()
        ..sort((a, b) => a.value.compareTo(b.value));
      var reversedEntries = entries.reversed.toList();
      double backgroundValue = 0.0;
      try {
        var backgroundEntry =
            reversedEntries.firstWhere((e) => e.key == "Background");
        backgroundValue = backgroundEntry.value;
      } catch (e) {
        // Background entry not found, proceed with default backgroundValue
      }

      classification = Map.fromEntries(
        reversedEntries.where((e) =>
            e.value >= _confidenceThreshold && (e.value >= backgroundValue)),
      );
      if (classification!.length == 1 &&
          classification!.containsKey("Background")) {
        classification = {
          "No weld detected": 1.0 - classification!["Background"]!
        };
      } else {
        classification!.remove("Background");
      }
    }
    final endTime = DateTime.now();
    final duration = endTime.difference(startTime);
    _fps = 1000 / duration.inMilliseconds;
    //print('Time taken: ${duration.inMilliseconds} ms');
    _isProcessing = false;
    if (mounted) {
      setState(() {});
    }
  }

  @override
  void initState() {
    WidgetsBinding.instance.addObserver(this);
    initCamera();
    imageClassificationHelper = ImageClassificationHelper();
    imageClassificationHelper.initHelper();
    super.initState();
  }

  @override
  Future<void> didChangeAppLifecycleState(AppLifecycleState state) async {
    switch (state) {
      case AppLifecycleState.paused:
        cameraController.stopImageStream();
        break;
      case AppLifecycleState.resumed:
        if (!cameraController.value.isStreamingImages) {
          await cameraController.startImageStream(imageAnalysis);
        }
        break;
      default:
    }
  }

  @override
  void dispose() {
    WidgetsBinding.instance.removeObserver(this);
    cameraController.dispose();
    imageClassificationHelper.close();
    super.dispose();
  }

  Widget cameraWidget(context) {
    var camera = cameraController.value;
    // fetch screen size
    final size = MediaQuery.of(context).size;

    // calculate scale depending on screen and camera ratios
    // this is actually size.aspectRatio / (1 / camera.aspectRatio)
    // because camera preview size is received as landscape
    // but we're calculating for portrait orientation
    var scale = size.aspectRatio * camera.aspectRatio;

    // to prevent scaling down, invert the value
    if (scale < 1) scale = 1 / scale;

    return Transform.scale(
      scale: scale,
      child: Center(
        child: CameraPreview(cameraController),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    // Size size = MediaQuery.of(context).size;
    List<Widget> list = [];

    list.add(
      SizedBox(
        child: (!cameraController.value.isInitialized)
            ? Container()
            : cameraWidget(context),
      ),
    );
    list.add(Align(
      alignment: Alignment.bottomCenter,
      child: SingleChildScrollView(
        child: Column(
          children: [
            if (classification != null)
              ...(classification!.entries.toList()
                    ..sort(
                      (a, b) => a.value.compareTo(b.value),
                    ))
                  .reversed
                  .take(3)
                  .map(
                    (e) => Container(
                      padding: const EdgeInsets.all(8),
                      color: Colors.white,
                      child: Row(
                        children: [
                          Text(e.key),
                          const Spacer(),
                          Text('${(e.value * 100).round()}%')
                        ],
                      ),
                    ),
                  ),
            if (classification == null)
              Container(
                padding: const EdgeInsets.all(8),
                color: Colors.white,
                child: const Row(
                  children: [
                    Text('Looking for welds...'),
                  ],
                ),
              ),
            if (_fps != null)
              Container(
                padding: const EdgeInsets.all(8),
                color: Colors.white,
                child: Row(
                  children: [
                    const Text('Performance'),
                    const Spacer(),
                    Text(_fps! < 1
                        ? '${(1 / _fps!).toStringAsFixed(2)} seconds'
                        : '${_fps!.toStringAsFixed(2)} FPS'),
                  ],
                ),
              ),
            // Add the slider widget
            Container(
              padding: const EdgeInsets.all(8),
              color: Colors.white,
              child: Row(
                children: [
                  const Text('Confidence Threshold'),
                  const Spacer(),
                  Expanded(
                    child: Slider(
                      value: _confidenceThreshold,
                      min: 0.0,
                      max: 1.0,
                      divisions: 100,
                      label: _confidenceThreshold.toStringAsFixed(2),
                      onChanged: (value) {
                        setState(() {
                          _confidenceThreshold = value;
                        });
                      },
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    ));

    return SafeArea(
      child: Stack(
        children: list,
      ),
    );
  }
}

import 'dart:developer';
import 'dart:io';

import 'package:firebase_ml_model_downloader/firebase_ml_model_downloader.dart';
import 'package:path_provider/path_provider.dart';

class ModelUpdater {
  final String modelName = 'weld';
  final String includedModel = "assets/models/weld_0.tflite";
  final String modelVersionKey = 'model_version';

  Future<File> getLocalModelFile(String version) async {
    final directory = await getApplicationDocumentsDirectory();
    return File('${directory.path}/${modelName}_$version.tflite');
  }

  Future<String> getLocalModelVersion() async {
    try {
      final directory = await getApplicationDocumentsDirectory();
      final versionFile = File('${directory.path}/$modelVersionKey');
      if (await versionFile.exists()) {
        return await versionFile.readAsString();
      }
    } catch (e) {
      log('Error reading local model version: $e');
    }
    return '0'; // Default version if not found
  }

  Future<void> downloadModel(String version) async {
    try {
      final customModel = await FirebaseModelDownloader.instance.getModel(
        '${modelName}_$version',
        FirebaseModelDownloadType.latestModel,
        FirebaseModelDownloadConditions(
          iosAllowsCellularAccess: true,
          iosAllowsBackgroundDownloading: false,
          androidChargingRequired: false,
          androidWifiRequired: false,
          androidDeviceIdleRequired: false,
        ),
      );

      final localModelFile = await getLocalModelFile(version);
      await customModel.file.copy(localModelFile.path);
      log('Model downloaded successfully');
    } catch (e) {
      log('Error downloading model: $e');
    }
  }

  Future<void> saveModelVersion(String version) async {
    final directory = await getApplicationDocumentsDirectory();
    final versionFile = File('${directory.path}/$modelVersionKey');
    await versionFile.writeAsString(version);
  }

  Future<void> checkAndUpdateModel() async {
    try {
      log('Checking for new models...');// TODO: Use firestore to keep track.
      final models = ["weld_0", "weld_1", "weld_2", "weld_3", "weld_4", "weld_5"];
      String latestVersion = '0';

      for (var model in models) {
        final modelName = model;
        if (modelName.startsWith(this.modelName)) {
          final version = modelName.split('_').last;
          if (int.tryParse(version) != null && int.parse(version) > int.parse(latestVersion)) {
            latestVersion = version;
          }
        }
      }

      final localVersion = await getLocalModelVersion();
      if (int.parse(latestVersion) > int.parse(localVersion)) {
        await downloadModel(latestVersion);
        await saveModelVersion(latestVersion);
      }
    } catch (e) {
      log('Error checking for model update: $e');
    }
  }

  Future<File> getModelFile() async {
    final localVersion = await getLocalModelVersion();
    final localModelFile = await getLocalModelFile(localVersion);

    if (await localModelFile.exists()) {
      return localModelFile;
    } else {
      return File(includedModel);
    }
  }
}

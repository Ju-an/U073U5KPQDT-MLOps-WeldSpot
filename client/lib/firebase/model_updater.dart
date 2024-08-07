import 'dart:developer';

import 'package:firebase_storage/firebase_storage.dart';
import 'package:image_classification_mobilenet/firebase_config.dart';
import 'package:path_provider/path_provider.dart';
import 'dart:io';

class ModelUpdater {
  final String modelStoragePath = 'models/';
  final String modelVersionKey = 'model_version';
  final String localModelName = 'mobilenet_quant.tflite';

  Future<File> getLocalModelFile() async {
    final directory = await getApplicationDocumentsDirectory();
    return File('${directory.path}/$localModelName');
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

  Future<String> getLatestRemoteModelVersion(FirebaseStorage storage) async {
    try {
      final ListResult result = await storage.ref(modelStoragePath).listAll();
      int latestVersion = 0;
      for (var item in result.items) {
        final String name = item.name;
        final RegExp versionRegex = RegExp(r'_v(\d+)\.tflite$');
        final Match? match = versionRegex.firstMatch(name);
        if (match != null) {
          final int version = int.parse(match.group(1)!);
          if (version > latestVersion) {
            latestVersion = version;
          }
        }
      }
      return latestVersion.toString();
    } catch (e) {
      log('Error fetching remote model version: $e');
    }
    return '0'; // Default version if not found
  }

  Future<void> downloadModel(FirebaseStorage storage, String version) async {
    try {
      final storageRef =
          storage.ref().child('$modelStoragePath/model_v$version.tflite');
      final localModelFile = await getLocalModelFile();
      await storageRef.writeToFile(localModelFile);
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
      log('Checking for new models...');
      final storage =
          FirebaseStorage.instanceFor(bucket: FirebaseStorageConfig.bucketName);
      final localVersion = await getLocalModelVersion();
      final remoteVersion = await getLatestRemoteModelVersion(storage);

      if (localVersion != remoteVersion) {
        await downloadModel(storage, remoteVersion);
        await saveModelVersion(remoteVersion);
      }

      // Verify the model file exists
      final localModelFile = await getLocalModelFile();
      if (await localModelFile.exists()) {
        log('Model file exists at ${localModelFile.path}');
      } else {
        log('Model file does not exist at ${localModelFile.path}');
      }
    } catch (e) {
      log('Error checking for model update: $e');
    }
  }
}

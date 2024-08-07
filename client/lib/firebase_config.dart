import 'dart:developer';

import 'package:firebase_core/firebase_core.dart';
import 'package:firebase_storage/firebase_storage.dart';

class FirebaseStorageConfig {
  // FILL FOLLOWING OPTIONS WITH YOURS:
  static const String hostAddress = '192.168.68.101'; // Change with yours
  static const int portNumber = 9199; // Change with yours
  // FILL FOLLOWING OPTIONS WITH YOURS FROM google-services.json:
  static const String apiKey =
      'AIzaSyDrL5X9UResq0OaKj9moxKSTlvd7tQcvrk'; // Change with yours
  static const String appId =
      '1:1095871114500:android:f5a785edab8b8da6abb451'; // Change with yours
  static const String messagingSenderId = '1095871114500'; // Change with yours
  static const String projectId = 'welding-defects-models'; // Change with yours
  static const String bucketName =
      'welding-defects-models.appspot.com'; // Change with yours (without the 'gs://')

  FirebaseStorageConfig._privateConstructor();

  // Static instance
  static final FirebaseStorageConfig _instance =
      FirebaseStorageConfig._privateConstructor();

  // Flag to check if already configured
  static bool _isConfigured = false;

  // Public method to access the instance
  static FirebaseStorageConfig get instance => _instance;

  Future<void> configure() async {
    if (!_isConfigured) {
      if (Firebase.apps.isEmpty) {
        await Firebase.initializeApp(
            name: "dev weld",
            options: const FirebaseOptions(
              apiKey: apiKey,
              appId: appId,
              messagingSenderId: messagingSenderId,
              projectId: projectId,
              storageBucket: bucketName,
            ));
      }
      log("Firebase initialized");
      //TODO: Remove emulator for deployment:
      FirebaseStorage.instanceFor(bucket: bucketName) //"gs://$bucketName"
          .useStorageEmulator(hostAddress, portNumber);
      log("Firebase Storage emulator configured");
      //FirebaseStorage.instanceFor(bucket: bucketName);
      _isConfigured = true;
    }
  }
}

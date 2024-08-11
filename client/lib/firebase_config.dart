import 'dart:developer';
import 'firebase_options.dart';
import 'package:firebase_core/firebase_core.dart';
import 'package:firebase_storage/firebase_storage.dart';

class FirebaseStorageConfig {
  // FILL FOLLOWING OPTIONS WITH YOURS:
  static const bool useEmulator = false; // Set to false for production, true for development
  static const String hostAddressEmulator = '192.168.1.102'; // Set to the IP of your machine that has the Storage emulator running
  static const int portNumberEmulator = 9199; // Change with the proper emulator port
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
            name: "app weld",
            options: DefaultFirebaseOptions.currentPlatform);
      }
      log("Firebase initialized");
      final storageBucket = DefaultFirebaseOptions.currentPlatform.storageBucket;
      final bucketName = storageBucket?.substring(0, storageBucket.indexOf('.appspot.com')) ?? '';
      final fsi = FirebaseStorage.instanceFor(bucket: bucketName);
      if(useEmulator) { //"gs://$bucketName"
        fsi.useStorageEmulator(hostAddressEmulator, portNumberEmulator);
      }
      log("Firebase Storage emulator configured");
      _isConfigured = true;
    }
  }
}

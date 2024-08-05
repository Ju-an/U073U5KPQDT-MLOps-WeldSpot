
# Installation

## Flutter (Frontend)

1. Access: https://docs.flutter.dev/get-started/install
2. In the flutter website, select the OS you downloaded the project (recommended to clone my repo on linux).
3. In the flutter website, for "Choose your first type of app" select **Android**.
4. Follow the instructions to install android sdk, build tools and flutter.

```
sudo apt update -y && sudo apt upgrade -y
sudo apt install -y curl git unzip xz-utils zip libglu1-mesa
sudo apt install -y libc6:amd64 libstdc++6:amd64 libbz2-1.0:amd64
sudo apt install -y lib32z1 libgtk-3-dev
sudo apt install -y android-sdk android-sdk-build-tools
sudo apt install -y clang cmake ninja-build pkg-config libgtk-3-dev
```

```
wget https://storage.googleapis.com/flutter_infra_release/releases/stable/linux/flutter_linux_3.22.3-stable.tar.xz
tar xf flutter_linux_3.22.3-stable.tar.xz
mv flutter $HOME/fluttersdk
export PATH="`pwd`/fluttersdk/bin:$PATH"
flutter --disable-analytics
flutter precache
rm flutter_linux_3.22.3-stable.tar.xz
sudo apt install google-android-cmdline-tools-10.0-installer
```
5. Install the Android SDK and accept license terms (y)

```
mkdir -p $HOME/Android/sdk/
sdkmanager --sdk_root=$HOME/Android/sdk "platform-tools" "platforms;android-34" "build-tools;34.0.0" "cmdline-tools;latest"
flutter config --android-sdk $HOME/Android/sdk
yes | sdkmanager --licenses
flutter doctor --android-licenses
flutter doctor
```

Final output should look like:
```
[✓] Flutter (Channel stable, 3.22.3, on Ubuntu 24.04 LTS 5.15.153.1-microsoft-standard-WSL2, locale C.UTF-8)
[✓] Android toolchain - develop for Android devices (Android SDK version 34.0.0)
[✓] Chrome - develop for the web
[✓] Linux toolchain - develop for Linux desktop
[!] Android Studio (not installed)*
[✓] Connected device (2 available)
[✓] Network resources
```

* Don't worry about Android Studio, we are using VS Code IDE.

## Firebase (Backend)
Install Firebase CLI (Requires NPM utility that comes from installing Node.js).
```ps
npm install -g firebase-tools
```

Install FlutterFire CLI
```ps
cd client
dart pub global activate flutterfire_cli
dart --disable-analytics
export PATH="$PATH":"$HOME/.pub-cache/bin"
```
You may see a message like: "Warning: Pub installs executables into C:\Users\<username>\AppData\Local\Pub\Cache\bin, which is not on your path." -> Add the path to your PATH environment variables.

Login to firebase account (You can create Spark Plan account with Google for 0$ - no monthly cost; aka free but limited resources)
```ps
firebase login
```

Initialize firebase in flutter project:
```ps
firebase init
```
* Select the features to use: Storage, Emulators.
* Create a new Firebase project to associate the flutter project.
* If error "Cloud resource location is not set", use Firebase Web Interface to set Cloud Storage product: https://console.firebase.google.com/u/0/project/<name-of-project>/storage -> Start
* Configure emulators with the default ports.


Create configuration file.
```ps
flutterfire configure
```

Activate firebase emulators
```ps
firebase emulators:start
```
Use the "Host:Port" (replace 127.0.0.1 with the IP of the machine running the emulator) for testing the app in your same network.

Use the "View in Emulator UI" URLs in web browser to manually manage the contents. If you open the "Storage" tab in the browser UI of the emulators (127.0.0.1:4000/storage), you can see default bucket URL like "gs://<firebase-project-name>.appspot.com".

Modify file `lib/firebase_config.dart` and use the proper IP and ports on your network. If wanting to deploy to cloud, replace with network addresses provided by Google's Firebase Web Console.

Inside the project there is also firebase.json -> Edit the emulators so they contain `"host": "0.0.0.0"` like this:
```json
{
  "storage": {
    "rules": "storage.rules"
  },
  "emulators": {
    "storage": {
      "port": 9199,
      "host": "0.0.0.0"
    },
    "ui": {
      "enabled": true
    },
    "singleProjectMode": true
  }
}
```
Ensure your machine has the required ports open. Optionally, you could run on Android Emulator instead of a real device.

Remember to remove firewall rules afterwards when not using project emulators.

### Configuring Android build

* Go to Firebase Console.
* Select Project.
* Click on the House icon.
* In the icons select the Android to add to app to start.
* For Android package name use: `org.tensorflow.image_classification_mobilenet`
* Register app.
* Download `google-services.json` file.
* Put the `google-services.json` file in `android/app` folder.
* Skip Steps: Firebase Web Console configuration to enable Firebase SDK with Android (Groovy build.gradle); files are already configured.
* Fill rest of `lib/firebase_config.dart` options according to the `google-services.json`:
```md
apiKey: From client > api_key > current_key.
appId: From client > client_info > mobilesdk_app_id.
messagingSenderId: From project_info > project_number.
projectId: From project_info > project_id.
storageBucket: From project_info > storage_bucket.
```

Rebuild flutter project:
```ps
flutter clean
flutter pub get
```

Fill the values in `android/app/src/main/res/values/values.xml` with the data in `google-services.json` and the ID of your project (default_web_client_id).
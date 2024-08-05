
# Installation

## TensorFlow with GPU support on NVIDIA GPUs (Linux Machine / WSL)

Install Miniconda (Python environment)
```sh
curl https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -o Miniconda3-latest-Linux-x86_64.sh

bash Miniconda3-latest-Linux-x86_64.sh
```

Create the environment for Python 3.10
```sh
conda create --name weld python=3.10
```

Start the environment before runing any pip or python code
```sh
conda activate weld
```

Install requirements
```sh
python -m pip install -U pip
pip install -r requirements
```

Test GPU support (ignore warnings printed)
```sh
python -c "import tensorflow as tf; print('********* AVAILABLE GPUS:', tf.config.list_physical_devices('GPU'), '*********')"
```
GPU printed should contain: `[PhysicalDevice(name='/physical_device:GPU:0', device_type='GPU')]`

## Flutter (Frontend) & Firebase (Backend)

Follow instructions to install Flutter: https://docs.flutter.dev/get-started/install

Install Firebase CLI (Requires NPM utility that comes from installing Node.js).
```ps
npm install -g firebase-tools
```

Install FlutterFire CLI
```ps
dart pub global activate flutterfire_cli
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
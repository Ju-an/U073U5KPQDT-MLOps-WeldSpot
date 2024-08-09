import subprocess
from flows.register_flows import register_flows
from options import FIREBASE_SDK_ADMIN_FILE_PATH, FIREBASE_STORAGE_BUCKET_NAME
from service.cloud_storage import init_firebase_storage

def main():
    print("Testing Firebase connectivity")
    storage = init_firebase_storage()
    print(FIREBASE_SDK_ADMIN_FILE_PATH, FIREBASE_STORAGE_BUCKET_NAME)
    print(storage)
    print("Launching TensorBoard service")
    subprocess.run(["tensorboard", "--logdir=logs/fit --port=6006"], check=True)
    print("Starting Collection and Modeling service.")
    register_flows()

if __name__ == "__main__":
    main()

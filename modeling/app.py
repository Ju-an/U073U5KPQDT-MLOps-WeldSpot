from options import FIREBASE_SDK_ADMIN_FILE_PATH, FIREBASE_STORAGE_BUCKET_NAME
from service.cloud_storage import delete_content, init_firebase_storage


def main():
    storage = init_firebase_storage()
    print(FIREBASE_SDK_ADMIN_FILE_PATH, FIREBASE_STORAGE_BUCKET_NAME)
    print(storage)
    delete_content(storage, "hello.txt")


if __name__ == "__main__":
    main()

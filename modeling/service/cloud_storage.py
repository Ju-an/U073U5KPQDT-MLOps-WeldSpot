"""
Module used for accessing remote storage from Firebase (using the Firebase Admin SDK) and from Roboflow.
"""
import os
import csv
import shutil
import roboflow
import firebase_admin
from firebase_admin import credentials, storage, ml

from options import ROBOFLOW_API_KEY, FIREBASE_SDK_ADMIN_FILE_PATH, FIREBASE_STORAGE_BUCKET_NAME, SPLIT_NAMES, RAW_PATH, TEMP_PATH

ROBOFLOW_WELDING_DATASET_WORKSPACE = "welding-2bplp"
ROBOFLOW_WELDING_DATASET_PROJECT = "weld-quality-inspection-rei9l"
ROBOFLOW_WELDING_DATASET_VERSION = 9

def init_firebase_storage():
    """
    Initializes Firebase storage with the provided credentials and storage bucket name.

    Returns:
        firebase_admin.storage.bucket.Bucket: The initialized Firebase storage bucket.
    """
    cred = credentials.Certificate(FIREBASE_SDK_ADMIN_FILE_PATH)
    firebase_admin.initialize_app(
        cred, {"storageBucket": f"{FIREBASE_STORAGE_BUCKET_NAME}.appspot.com"}
    )

    bucket = storage.bucket()

    return bucket


def upload_content(storage, content, filename, public=False):
    # Add file to firebase storage bucket
    blob = storage.blob(filename)

    # Upload the content to the blob
    blob.upload_from_string(content)

    # Make the blob publicly accessible (optional)
    if public:
        blob.make_public()

    print(f"File uploaded to {blob.public_url}")


def read_content(storage, filename):
    # Get the blob with the given filename
    blob = storage.blob(filename)

    # Download the blob's content as a string
    content = blob.download_as_string()

    return content


def delete_content(storage, filename):
    # Get the blob with the given filename
    blob = storage.blob(filename)

    # Delete the blob
    blob.delete()

    print(f"File {filename} deleted")


def download_roboflow(path = RAW_PATH):
    """
    Downloads the Roboflow Welding dataset to the specified path.

    Args:
        path (str): The path to save the downloaded dataset to.
    """
    rf = roboflow.Roboflow(api_key=ROBOFLOW_API_KEY)
    project = rf.workspace(ROBOFLOW_WELDING_DATASET_WORKSPACE).project(ROBOFLOW_WELDING_DATASET_PROJECT)
    version = project.version(ROBOFLOW_WELDING_DATASET_VERSION)
    version.download(model_format="multiclass", location=TEMP_PATH)
    # Process each split index csv
    count = 0
    for split in SPLIT_NAMES:
        csv_path = os.path.join(TEMP_PATH, split, "_classes.csv")
        with open(csv_path, mode='r') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Skip the header row
            for row in reader:
                image_name = row[0]
                image_path = os.path.join(TEMP_PATH, split, image_name)
                count += 1
                classes = "_".join([r.strip() for r in row[1:]]) # First is the file name.
                dest_name = f"{count}_0_{classes}.jpg" # All are non-background.
                dest_path = os.path.join(path, dest_name)
                shutil.copy(image_path, dest_path)
    shutil.rmtree(TEMP_PATH)
    return count

def download_firebase(path = RAW_PATH):
    bucket = init_firebase_storage()
    count = 0

    blobs = bucket.list_blobs()
    blobs = [blob for blob in blobs if blob.name.endswith(".jpg")]
    path = "data/raw"
    os.makedirs(path, exist_ok=True)

    for blob in blobs:
        file_path = os.path.join(path, blob.name)
        blob.download_to_filename(file_path)
        blob.delete()
        count += 1

    return count

def upload_tflite(model_path, model_tags):
    bucket = init_firebase_storage()
    model_name = os.path.splitext(os.path.basename(model_path))[0]
    source = ml.TFLiteGCSModelSource.from_tflite_model_file(model_path)
    tflite_format = ml.TFLiteFormat(model_source=source)
    model = ml.Model(
        display_name=model_name,
        tags=model_tags,
        model_format=tflite_format)
    new_model = ml.create_model(model)
    ml.publish_model(new_model.model_id)

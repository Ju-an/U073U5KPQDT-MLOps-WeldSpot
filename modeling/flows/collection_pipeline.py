from service.cloud_storage import download_firebase, download_roboflow
from service.image_transformations import preprocess_images, augment_images, split_images
from service.metric_monitoring import drift_detection
from prefect import task, flow
from prefect.events import emit_event
from prefect.task_runners import SequentialTaskRunner
import os, zipfile, shutil
from datetime import datetime

from options import CLASS_NAMES, SPLIT_NAMES, RAW_PATH, PROCESSED_PATH, AUGMENTED_PATH, SPLIT_PATH

DATA_DIR = "data"
INITIAL_ZIP = "data/initial.zip"
INITIAL_PATH = "data/initial"

def empty_folder(path):
    """
    Empties images in the directory.
    """
    count = 0
    for image in os.listdir(path):
        file_path = os.path.join(path, image)
        if os.path.isfile(file_path):
            os.remove(file_path)
            count += 1
    return count

@task
def download_files_initial():
    """
    Downloads the initial dataset from Roboflow and extracts our background images zip.
    """
    with zipfile.ZipFile(INITIAL_ZIP, 'r') as zip_ref:
            zip_ref.extractall(DATA_DIR)
    downloaded = download_roboflow()
    print(f"Downloaded {downloaded} images from Roboflow.")
    return downloaded

@task
def download_files():
    """
    Retrieves new images from Firebase.
    """
    count = download_firebase()
    print(f"Downloaded and deleted {count} images from Firebase.")
    return count

@task
def preprocess_files():
    processed = preprocess_images()
    deleted = empty_folder(RAW_PATH)
    print(f"Preprocessed {processed}/{deleted} images.")
    return processed

@task
def augment_files(augments=1):
    augmented, total = augment_images(augments)
    deleted = empty_folder(PROCESSED_PATH)
    print(f"Augmented {augmented}/{deleted} images.")
    return total

@task
def split_files(destination=INITIAL_PATH):
    split = split_images(destination)
    deleted = empty_folder(AUGMENTED_PATH)
    print(f"Split {split}/{deleted} images.")
    return split

@flow(name="Initial Dataset Collection Pipeline", task_runner=SequentialTaskRunner(), log_prints=True, retries=5, retry_delay_seconds=15)
def initial_dataset_flow():
    download_initial = download_files_initial()
    if download_initial == 0:
        print("Skipping after no initial images downloaded.")
        return
    preprocess = preprocess_files()
    if preprocess == 0:
        print("Skipping after no initial images preprocessed.")
        return
    augment = augment_files(1)
    if augment == 0:
        print("Skipping after no initial images augmented.")
        return
    split_initial = split_files()
    if split_initial == 0:
        print("No initial images to split.")

@flow(name="Daily Dataset Collection Pipeline", task_runner=SequentialTaskRunner(), log_prints=True, retries=3, retry_delay_seconds=10)
def periodic_monitoring_flow():
    download = download_files()
    if download == 0:
        print("Skipping after no cloud images downloaded.")
        return
    metrics, drift = drift_detection()
    if metrics is not None:
        print("Metrics obtained:")
        for class_name, m in metrics.items():
            print(f"{class_name}: {m}")
    if drift is None:
        print("skipping after no drift detected.")
        return
    preprocess = preprocess_files()
    if preprocess == 0:
        print("Skipping after no images preprocess.")
        return
    augment = augment_files(8)
    if augment == 0:
        print("Skipping after no images preprocess.")
        return
    split = split_files(destination=f"{SPLIT_PATH}/{datetime.now().strftime('%Y%m%d')}/")
    if split == 0:
        print("No images to split.")
        return
    if drift is not None:
        emit_event(event="drift.detected", resource={"prefect.resource.id": "dataset.auc", "prefect.resource.name": drift})

if __name__ == "__main__":
    print("Testing dataset integration.")
    download_files_initial()
    preprocess_files()
    augment_files(1)
    split_files("temp")
    # empty_folder("temp")
    print("Cleaning up temporary dataset.\nTesting drift integration.")
    download_files()
    metrics, drift = drift_detection()
    print(f"· Metrics: {metrics}\n· Drift: {drift}")

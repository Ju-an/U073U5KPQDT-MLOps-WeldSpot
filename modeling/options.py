"""
Module for configuring the dataset service.
"""

import os
from pathlib import Path  # For making absolute paths

from dotenv import load_dotenv

load_dotenv()  # Load the .env file

# Loading the credentials for the remote services
FIREBASE_SDK_ADMIN_FILE_PATH = Path(__file__).parent / "private/serviceAdmin.json"
FIREBASE_STORAGE_BUCKET_NAME = os.environ.get("FIREBASE_STORAGE_BUCKET")
ROBOFLOW_API_KEY = os.environ.get("ROBOFLOW_API_KEY")

# Batch size = the number of images passed together to the train step (higher = faster but more memory)
TRAIN_BATCH_SIZE = os.environ.get("BATCH_SIZE", 160)  # Load from .env file or use default value 16.
TRAIN_EPOCHS = os.environ.get("EPOCHS", 10)  # More epochs = more training (better but slower)

# Verbosity of the training process.
TRAINING_VERBOSITY = 1 # 0 = silent, 1 = single progress bar, 2 = one progress per epoch (most detailed)
# Threshold for considering an image as a class.
CLASS_THRESHOLD = 0.6  # For example, in inference, 0.6 (60%) chance of being a class or above to consider it.
# Threshold for detecting drift in AUC. AUC (Area Under the Curve) is a metric.
AUC_THRESHOLD = 0.75  # If evaluation AUC is below this value, drift is detected and retrain is required.

SPLIT_TRAIN = 0.8  # Percentage of the dataset used for training
SPLIT_VALID = 0.15  # Percentage of the dataset used for validation
SPLIT_TEST = 0.05  # Percentage of the dataset used for testing and evaluation

TEMP_PATH = "tmp"  # Folder for temporary files
# Number of (additional) augmented images generated from each image
AUGMENTATION_INCREASE = 8
# The target size of the images used by the model (higher = more accurate but slower to train/infer)
TARGET_SIZE = (256,256)

# Don't change the following:
# Stores the initial dataset downloaded from Roboflow
INITIAL_PATH = "data/initial"
# Stores unclassified original images downloaded at first (formated as <id>_<class1>_..._<class7>.jpg)
RAW_PATH = "data/raw"
# Stores images from raw get after being processed to remove noise and resized.
PROCESSED_PATH = "data/processed"
# Stores images from processed after they get augmented to increase the size of the dataset (1 image generates 8 new images = 9 total)
AUGMENTED_PATH = "data/augmented"
# Stores images from augmented that get split into training, validation, and test sets and into their classes
SPLIT_PATH = "data/splits"

SPLIT_NAMES = ["train", "valid", "test"]  # Folders names for image splits.
CLASS_NAMES = [
    "Background",
    "Bad Welding",
    "Crack",
    "Excess Reinforcement",
    "Good Welding",
    "Porosity",
    "Splatters",
]  # Names of the classes predicted from 0 to 6.

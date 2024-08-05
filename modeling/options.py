"""
Module for configuring the dataset service.
"""

import os
from pathlib import Path  # For making absolute paths

from dotenv import load_dotenv

load_dotenv()

# Loading the credentials for the remote services
FIREBASE_SDK_ADMIN_FILE_PATH = Path(__file__).parent / "private/serviceAdmin.json"
FIREBASE_STORAGE_BUCKET_NAME = os.environ.get("FIREBASE_STORAGE_BUCKET")
ROBOFLOW_API_KEY = os.environ.get("ROBOFLOW_API_KEY")

TRAIN_BATCH_SIZE = os.environ.get("BATCH_SIZE", 32)
TRAIN_EPOCHS = os.environ.get("EPOCHS", 10)

CLASS_THRESHOLD = 0.6 # Threshold for considering an image as a class. For example, in inference, 0.6 (60%) chance of being a class or above to consider
AUC_THRESHOLD = 0.75 # Threshold for detecting drift in AUC. If evaluation AUC is below this value, drift is detected and retrain is required

SPLIT_TRAIN = 0.8 # Percentage of the dataset used for training
SPLIT_VALID = 0.15 # Percentage of the dataset used for validation
SPLIT_TEST = 0.05 # Percentage of the dataset used for testing and evaluation

TEMP_PATH = "temp" # For temporary files
AUGMENTATION_INCREASE = 8 # Number of (additional) augmented images generated from each image
TARGET_SIZE = (256, 256) # The target size of the images used by the model

RAW_PATH = "data/raw" # Stores unclassified original images downloaded at first (formated as <id>_<class1>_..._<class7>.jpg)
PROCESSED_PATH = "data/processed" # Stores images from raw get after being processed to remove noise and resized.
AUGMENTED_PATH = "data/augmented" # Stores images from processed after they get augmented to increase the size of the dataset (1 image generates 8 new images = 9 total)
SPLIT_PATH = "data/split" # Stores images from augmented that get split into training, validation, and test sets and into their classes


CLASS_NAMES = ["Background", "Bad Welding", "Crack", "Excess Reinforcement", "Good Welding", "Porosity", "Splatters"] # Don't change
SPLIT_NAMES = ["train", "valid", "test"] # Don't change

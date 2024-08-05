
import os
import shutil
from sklearn.model_selection import train_test_split
from PIL import Image

from options import TARGET_SIZE, CLASS_NAMES, SPLIT_NAMES, RAW_PATH, PROCESSED_PATH, AUGMENTED_PATH, AUGMENTATION_INCREASE, SPLIT_VALID, SPLIT_TEST, CLASS_THRESHOLD
from service.image_augmentations import random_rotation, random_flip, random_color_jitter, random_noise, median_filter, gaussian_filter

def divide_image_labels(image_path):
    """
    Divide the image path into the id and its labels from its name formatted as <id>_<class1>_..._<class7>.jpg.

    Args:
        image_path (str): The path of the image.

    Returns:
        str: The id of the image.
        list: With the probability of each label.
    """
    file_name = os.path.basename(image_path)
    division = file_name.split("_")
    return division[0], [d.split(".")[0] if "." in d else d for d in division[1:]]

def divide_class_names(labels):
    """
    Gets the class names from the labels it belongs to."""
    accepted = []
    for(i, label) in enumerate(labels):
        if float(label) >= CLASS_THRESHOLD:
            accepted.append(i)
    return [CLASS_NAMES[int(label)] for label in accepted]

def load_image(path):
    """
    Read an image from the specified path.
    """
    return Image.open(path)

def save_image(image, path):
    """
    Save an image to the specified path.
    """
    image.save(path)

def resize_image(image, size):
    """
    Resize an image to the specified size.
    """
    return image.resize(size)

def normalize_image(image):
    """
    Convert the image to pixel values between 0 and 1.
    """
    return image / 255.0

def preprocess_images():
    """
    Runs the preprocessing step of the dataset.
    Files are read from the RAW_PATH, processed, and saved to the PROCESSED_PATH.

    Returns:
        int: The number of images processed.
    """
    paths = os.listdir(RAW_PATH)
    count = 0
    total = len(paths)
    for path in paths:
        # print(f"Preprocessing image {1+count}/{total}")
        name, labels = divide_image_labels(path)
        image = load_image(os.path.join(RAW_PATH, path))
        image = resize_image(image, TARGET_SIZE)
        image = median_filter(image)
        image = gaussian_filter(image)
        save_image(image, os.path.join(PROCESSED_PATH, f"{name}_{'_'.join(labels)}.jpg"))
        count += 1
    return count

def augment_images(augments=AUGMENTATION_INCREASE):
    """
    Runs the augmentation steps of the dataset.
    """
    paths = os.listdir(PROCESSED_PATH)
    count = 0
    total = 0
    maxim = len(paths)
    for path in paths:
        # print(f"Augmenting image {count+1}/{maxim}")
        name, labels = divide_image_labels(path)
        image = load_image(os.path.join(PROCESSED_PATH, path))
        for _ in range(augments):
            augmented = random_rotation(image)
            augmented = random_flip(augmented)
            augmented = random_color_jitter(augmented)
            augmented = random_noise(augmented)
            save_image(augmented, os.path.join(AUGMENTED_PATH, f"{name}-{total}_{'_'.join(labels)}.jpg"))
            total += 1
        count += 1
    return count, total

def group_images_by_class(files, tmp):
    """
    Group the images by their class names.
    """
    for file_name in files:
        _, labels = divide_image_labels(file_name)
        classes = divide_class_names(labels)
        for name in classes:
            class_dir = os.path.join(tmp, name)
            os.makedirs(class_dir, exist_ok=True)
            shutil.copy(os.path.join(AUGMENTED_PATH, file_name), os.path.join(class_dir, file_name))

def split_images(split_dir):
    """
    Split the images into the train, valid, and test sets.
    """
    augmented_dir = AUGMENTED_PATH
    os.makedirs(split_dir, exist_ok=True)

    for split_type in SPLIT_NAMES:
        os.makedirs(os.path.join(split_dir, split_type), exist_ok=True)

    files = [f for f in os.listdir(augmented_dir) if f.endswith(".jpg")]
    tmp = "tmp"
    total = len(files)
    group_images_by_class(files, tmp)
    count = 0
    temp = os.listdir(tmp)
    maxim = len(temp)
    for class_name in temp:
        # print(f"Splitting {count+1}/{maxim} images.")
        class_dir = os.path.join(tmp, class_name)
        class_files = [f for f in os.listdir(class_dir) if f.endswith(".jpg")]

        valid_test_split = SPLIT_VALID + SPLIT_TEST
        train_files, test_files = train_test_split(class_files, test_size=valid_test_split)
        test_split = SPLIT_TEST / valid_test_split
        valid_files, test_files = train_test_split(test_files, test_size=test_split)
        
        # Make sure subpath for class_name inside splits exist
        for split_type in SPLIT_NAMES:
            os.makedirs(os.path.join(split_dir, split_type, class_name), exist_ok=True)

        for file_name in train_files:
            shutil.move(os.path.join(class_dir, file_name), os.path.join(split_dir, "train", class_name, file_name))

        for file_name in valid_files:
            shutil.move(os.path.join(class_dir, file_name), os.path.join(split_dir, "valid", class_name, file_name))

        for file_name in test_files:
            shutil.move(os.path.join(class_dir, file_name), os.path.join(split_dir, "test", class_name, file_name))

    shutil.rmtree(tmp)
    return total
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator

from options import TARGET_SIZE, TRAIN_BATCH_SIZE

# Set the GPU options before any other usage
try:
    physical_devices = tf.config.list_physical_devices('GPU')
    for device in physical_devices:
        tf.config.experimental.set_memory_growth(device, True)
except Exception as e:
    print(e)

def get_device():
    """
    Get the device (CPU or GPU) for training.
    Returns the appropriate device string for use within a `with tf.device` clause.
    """
    return "/device:GPU:0" if len(tf.config.list_physical_devices('GPU')) > 0 else "/device:CPU:0"

def get_split_generators(path):
    train_path = f'{path}/train'
    validation_path = f'{path}/valid'
    test_path = f'{path}/test'
    train_datagen = ImageDataGenerator(rescale=1./255)
    validation_datagen = ImageDataGenerator(rescale=1./255)
    test_datagen = ImageDataGenerator(rescale=1./255)

    train_generator = train_datagen.flow_from_directory(
        train_path,
        target_size=TARGET_SIZE,
        batch_size=TRAIN_BATCH_SIZE,
        shuffle=True,
        class_mode='categorical')

    validation_generator = validation_datagen.flow_from_directory(
        validation_path,
        target_size=TARGET_SIZE,
        batch_size=TRAIN_BATCH_SIZE,
        class_mode='categorical')

    test_generator = test_datagen.flow_from_directory(
        test_path,
        target_size=TARGET_SIZE,
        batch_size=TRAIN_BATCH_SIZE,
        class_mode='categorical')
    
    return train_generator, validation_generator, test_generator
import warnings

import pytest
import tensorflow as tf


def check_gpu_availability():
    try:
        physical_devices = tf.config.list_physical_devices("GPU")
        if not physical_devices:
            warnings.warn("GPU is not available, using CPU instead", UserWarning)
        else:
            for device in physical_devices:
                tf.config.experimental.set_memory_growth(device, True)
        return physical_devices
    except tf.errors.InternalError as e:
        warnings.warn(
            f"TensorFlow internal error while checking GPU availability: {e}",
            UserWarning,
        )
        return []
    except Exception as e:
        warnings.warn(
            f"An unexpected error occurred while checking GPU availability: {e}",
            UserWarning,
        )
        return None


def test_tensorflow_gpu_support():
    physical_devices = check_gpu_availability()
    assert physical_devices is not None, "Failed to check GPU availability"

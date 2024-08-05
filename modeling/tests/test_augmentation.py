import pytest
from PIL import Image
import numpy as np

from service.image_augmentations import clip_image, median_filter, gaussian_filter, poisson_noise, salt_and_pepper_noise, random_rotation, random_flip, random_color_jitter, random_noise

@pytest.fixture
def sample_image():
    # Create a simple 100x100 image with random colors
    data = np.random.randint(0, 256, (100, 100, 3), dtype=np.uint8)
    return Image.fromarray(data)

def test_clip_image(sample_image):
    image_array = np.array(sample_image)
    clipped_image = clip_image(image_array)
    assert np.all(np.array(clipped_image) >= 0)
    assert np.all(np.array(clipped_image) <= 255)

def test_median_filter(sample_image):
    filtered_image = median_filter(sample_image)
    assert isinstance(filtered_image, Image.Image)

def test_gaussian_filter(sample_image):
    filtered_image = gaussian_filter(sample_image)
    assert isinstance(filtered_image, Image.Image)

def test_poisson_noise(sample_image):
    noisy_image = poisson_noise(sample_image)
    assert isinstance(noisy_image, Image.Image)

def test_salt_and_pepper_noise(sample_image):
    noisy_image = salt_and_pepper_noise(sample_image)
    assert isinstance(noisy_image, Image.Image)

def test_random_rotation(sample_image):
    rotated_image = random_rotation(sample_image)
    assert isinstance(rotated_image, Image.Image)

def test_random_flip(sample_image):
    flipped_image = random_flip(sample_image)
    assert isinstance(flipped_image, Image.Image)

def test_random_color_jitter(sample_image):
    jittered_image = random_color_jitter(sample_image)
    assert isinstance(jittered_image, Image.Image)

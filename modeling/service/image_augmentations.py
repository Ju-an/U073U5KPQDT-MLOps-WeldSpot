import random

import numpy as np
from PIL import Image, ImageEnhance, ImageFilter


def clip_image(image_array):
    """
    Clip the pixel values so they are between 0 and 255.
    """
    return Image.fromarray(image_array.astype(np.uint8))


def median_filter(image, size=3):
    """
    Apply a median filter to the image to reduce spikes.
    """
    return image.filter(ImageFilter.MedianFilter(size=size))


def gaussian_filter(image, radius=1):
    """
    Apply a gaussian smooth to the image to reduce noise.
    """
    return image.filter(ImageFilter.GaussianBlur(radius=radius))


def poisson_noise(image, scale=0.99):
    """
    Apply poisson noise to the image.
    """
    image_array = np.array(image)
    noisy_image = np.random.poisson(image_array * scale) / float(scale)
    noisy_image = np.clip(noisy_image, 0, 255).astype(np.uint8)
    return Image.fromarray(noisy_image)


def salt_and_pepper_noise(image, amount=0.001):
    """
    Apply salt and pepper noise to the image.
    """
    image_array = np.array(image)
    row, col, _ = image_array.shape
    num_salt = np.ceil(amount * image_array.size * 0.5)
    num_pepper = np.ceil(amount * image_array.size * 0.5)

    # Add salt
    coords = [np.random.randint(0, i - 1, int(num_salt)) for i in image_array.shape]
    image_array[coords[0], coords[1], :] = 255

    # Add pepper
    coords = [np.random.randint(0, i - 1, int(num_pepper)) for i in image_array.shape]
    image_array[coords[0], coords[1], :] = 0

    return clip_image(image_array)


def random_rotation(image, range=12):
    """
    Apply a random arbitrary rotation to the image.
    """
    angle = random.uniform(-range, range)
    return image.rotate(angle)


def random_flip(image, chance=0.5):
    """
    Apply randomly horizontal and vertical flips to the image.
    """
    if random.random() < chance:
        image = image.transpose(Image.FLIP_LEFT_RIGHT)
    if random.random() < chance:
        image = image.transpose(Image.FLIP_TOP_BOTTOM)
    return image


def random_color_jitter(image, range=0.001):
    """
    Apply random color jitter to the image (brightness, saturation, hue).
    """
    enhancer = ImageEnhance.Brightness(image)
    image = enhancer.enhance(1 + random.uniform(-range, range))
    enhancer = ImageEnhance.Color(image)
    image = enhancer.enhance(1 + random.uniform(-range, range))
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(1 + random.uniform(-range, range))
    return image


def random_noise(image):
    """
    Apply randomly a noise from the vailable (gaussian, poisson, or s&p).
    """
    noise_functions = [gaussian_filter, poisson_noise, salt_and_pepper_noise]
    noise_function = random.choice(noise_functions)
    return noise_function(image)

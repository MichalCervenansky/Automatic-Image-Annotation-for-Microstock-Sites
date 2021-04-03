import cv2
import numpy as np
import tensorflow as tf

RESIZE_TO = 224


def preprocess_image(images):
    images = np.array(images)
    tmp = images.shape
    # reshape into shape [batch_size, height, width, num_channels]
    img_reshaped = tf.reshape(images, [images.shape[0], images.shape[1], images.shape[2], images.shape[3]])
    # Use `convert_image_dtype` to convert to floats in the [0,1] range.
    images = tf.image.convert_image_dtype(img_reshaped, tf.float32)
    return images


def convert_image(img_paths):
    # Load a testing images:
    images = []
    for img in img_paths:
        images.append(tf.image.resize(cv2.imread(img), [RESIZE_TO, RESIZE_TO]))
    images = tf.image.convert_image_dtype(images, tf.float32)
    images = preprocess_image(images)

    return images

# For running inference on the TF-Hub module.
import tensorflow as tf

from PIL import Image

from utils.object_cropping import crop_out_boxes
from utils.object_detection_utils import load_img, create_filtered_dic, filter_result, draw_boxes
import config as c


def run_detector(path, detector):
    img = load_img(path)
    converted_img = tf.image.convert_image_dtype(img, tf.float32)[tf.newaxis, ...]


    result = detector(converted_img)
    result = {key: value.numpy() for key, value in result.items()}
    filtered_dic = create_filtered_dic(filter_result(result, c.OD_PRECISION_THRESHOLD, c.OD_MAX_BOXES), result)

    image_with_boxes = draw_boxes(
        img.numpy(), filtered_dic["detection_boxes"],
        filtered_dic["detection_class_entities"], filtered_dic["detection_scores"])

    crop_out_boxes(img.numpy(), filtered_dic["detection_boxes"])

    Image.fromarray(image_with_boxes).save(c.TEMP_PATH + "image_with_boxes.jpg")

    return set(filtered_dic["detection_class_entities"])

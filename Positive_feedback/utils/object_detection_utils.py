import tensorflow as tf
from PIL import ImageColor, ImageFont, Image, ImageDraw
import numpy as np


def load_img(path):
    img = tf.io.read_file(path)
    img = tf.image.decode_jpeg(img, channels=3)
    return img


def filter_result(result, min_score, max_boxes):
    accepted_indexes = []
    num = 0
    for index in range(len(result["detection_scores"])):
        if result["detection_scores"][index] > min_score and num < max_boxes:
            accepted_indexes.append(index)
            num += 1
    return accepted_indexes


def create_filtered_dic(accepted_indexes, orig_result):
    filtered_dic = {"detection_scores": [], "detection_boxes": [], "detection_class_entities": []}

    for index in accepted_indexes:
        filtered_dic["detection_scores"].append(orig_result["detection_scores"][index])
        filtered_dic["detection_boxes"].append(orig_result["detection_boxes"][index])
        filtered_dic["detection_class_entities"].append(orig_result["detection_class_entities"][index])
    return filtered_dic


def draw_bounding_box_on_image(image,
                               ymin,
                               xmin,
                               ymax,
                               xmax,
                               color,
                               font,
                               thickness=4,
                               display_str_list=()):
    """Adds a bounding box to an image."""
    draw = ImageDraw.Draw(image)
    im_width, im_height = image.size
    (left, right, top, bottom) = (xmin * im_width, xmax * im_width,
                                  ymin * im_height, ymax * im_height)
    draw.line([(left, top), (left, bottom), (right, bottom), (right, top),
               (left, top)],
              width=thickness,
              fill=color)

    # If the total height of the display strings added to the top of the bounding
    # box exceeds the top of the image, stack the strings below the bounding box
    # instead of above.
    display_str_heights = [font.getsize(ds)[1] for ds in display_str_list]
    # Each display_str has a top and bottom margin of 0.05x.
    total_display_str_height = (1 + 2 * 0.05) * sum(display_str_heights)

    if top > total_display_str_height:
        text_bottom = top
    else:
        text_bottom = top + total_display_str_height
    # Reverse list and print from bottom to top.
    for display_str in display_str_list[::-1]:
        text_width, text_height = font.getsize(display_str)
        margin = np.ceil(0.05 * text_height)
        draw.rectangle([(left, text_bottom - text_height - 2 * margin),
                        (left + text_width, text_bottom)],
                       fill=color)
        draw.text((left + margin, text_bottom - text_height - margin),
                  display_str,
                  fill="black",
                  font=font)
        text_bottom -= text_height - 2 * margin


def draw_boxes(image, boxes, class_names, scores):
    """Overlay labeled boxes on an image with formatted scores and label names."""
    colors = list(ImageColor.colormap.values())

    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSansNarrow-Regular.ttf",
                                  25)
    except IOError:
        font = ImageFont.load_default()

    for i in range(len(boxes)):
        ymin, xmin, ymax, xmax = tuple(boxes[i])
        display_str = "{}: {}%".format(class_names[i].decode("ascii"),
                                       int(100 * scores[i]))
        color = colors[hash(class_names[i]) % len(colors)]
        image_pil = Image.fromarray(np.uint8(image)).convert("RGB")
        draw_bounding_box_on_image(
            image_pil,
            ymin,
            xmin,
            ymax,
            xmax,
            color,
            font,
            display_str_list=[display_str])
        np.copyto(image, np.array(image_pil))
    return image

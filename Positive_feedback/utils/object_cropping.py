import os
import shutil

from PIL import Image
import config as c


# Out of bound will be deal with later using
def prepare_crop(im_width, im_height, box):
    ymin, xmin, ymax, xmax = tuple(box)
    margin = 10
    left, right, top, bottom = (round(xmin * im_width + margin), round(xmax * im_width + margin),
                                round(ymin * im_height + margin), round(ymax * im_height + margin))
    box_width = right - left
    box_height = bottom - top
    if box_width > box_height:
        diff = box_width - box_height
        top -= diff // 2
        bottom += diff // 2
    elif box_width < box_height:
        diff = box_height - box_width
        left -= diff // 2
        right += diff // 2

    if left < 0:
        left -= left
        right += left
    if right > im_width:
        right -= right - im_width
        left -= right-im_width
    if top < 0:
        top -= top
        bottom += top
    if bottom > im_height:
        bottom -= bottom-im_height
        top -= bottom-im_height

    return left, right, top, bottom


def crop_out_boxes(image, boxes):
    im_width, im_height = image.shape[1], image.shape[0]  # x,y flipped due to numpy array
    i = 0
    if os.path.exists(c.TEMP_PATH):
        shutil.rmtree(c.TEMP_PATH)
    os.mkdir(c.TEMP_PATH)
    for box in boxes:
        i += 1
        left, right, top, bottom = prepare_crop(im_width, im_height, box)
        crop_img = Image.fromarray(image[top:bottom, left:right])
        crop_img.save(c.TEMP_PATH + 'boxes_' + str(i) + '.jpg')

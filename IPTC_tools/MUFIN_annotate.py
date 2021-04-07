import base64
import os
import urllib.parse
import requests
from xml.etree import ElementTree
import pandas as pd
import configuration as c

from utils.anotate_utils import prep_boxes, write_iterable_to_file, load_big_image_feedback, parse_muffin_annotation, \
    convert_file_into_dic, resize_as_binary_image


def mufin_annotate(path):
    tmp_image = resize_as_binary_image(path)
    with open(tmp_image, "rb") as f:
        opened_binary_file = f.read()
        img_encoded = urllib.parse.quote(base64.b64encode(opened_binary_file).decode('ascii'))
        big_image_url = c.URL_WITH_PARAMS + "&keywords=" + load_big_image_feedback() + "&url=data:image/jpeg;base64," + img_encoded
        big_image = parse_muffin_annotation(ElementTree.fromstring(requests.get(big_image_url).content))
        write_iterable_to_file(big_image, c.TEMP_PATH + "big_image_keywords.txt")
    os.remove(tmp_image)

    C_dic = convert_file_into_dic(c.TEMP_PATH + "C_results.txt")
    OD_dic = convert_file_into_dic(c.TEMP_PATH + "OD_results.txt")
    boxes = prep_boxes()
    result = pd.DataFrame(big_image)

    for box in boxes:
        tmp_image = resize_as_binary_image(box)
        with open(tmp_image, "rb") as f:
            opened_binary_file = f.read()
            img_encoded = urllib.parse.quote(base64.b64encode(opened_binary_file).decode('ascii'))
            fed = ' '.join([str(elem) for elem in C_dic[os.path.basename(box)] + OD_dic[os.path.basename(box)]])
            if fed:
                box_url = c.URL_WITH_PARAMS + "&keywords=" + fed + "&url=data:image/jpeg;base64," + img_encoded
            else:
                box_url = c.URL_WITH_PARAMS + "&url=data:image/jpeg;base64," + img_encoded
            box_res = parse_muffin_annotation(ElementTree.fromstring(requests.get(box_url).content))
            write_iterable_to_file(box_res, box.replace(".jpg", "_res.txt"))
            result = result.append(box_res)

    return result

import base64
import os

import requests
from xml.etree import ElementTree
import pandas as pd
import configuration as c

from utils.anotate_utils import prep_boxes, write_iterable_to_file, load_big_image_feedback, parse_muffin_annotation, \
    convert_file_into_dic, parse_class, resize_as_binary_image


def mufin_annotate(path):
    tmp_image = resize_as_binary_image(path)
    with open(tmp_image, "rb") as f:
        opened_binary_file = f.read()
        big_image_url = c.URL_WITH_PARAMS + "&keywords=" + load_big_image_feedback() + "&url=data:image/jpeg;base64," + base64.b64encode(opened_binary_file).decode('utf-8')
        tmp_encoded = base64.b64encode(opened_binary_file).decode('utf-8')
        tmp_len = len(tmp_encoded)
        tmp_req_result = requests.get(big_image_url).content
        big_image = parse_muffin_annotation(ElementTree.fromstring(requests.get(big_image_url).content))
        write_iterable_to_file(big_image, c.TEMP_PATH + "big_image_keywords.txt")
    os.remove(tmp_image)

    C_dic = convert_file_into_dic(c.TEMP_PATH + "C_results.txt")
    OD_dic = convert_file_into_dic(c.TEMP_PATH + "OD_results.txt")
    boxes = prep_boxes()
    result = pd.DataFrame(big_image)

    for box in boxes:
        fed = [parse_class(C_dic[box]), parse_class(OD_dic[box])]
        box_url = c.URL_WITH_PARAMS + "&keywords=" + fed + "url=data:image/jpeg;base64," + str(base64.b64encode(
            resize_as_binary_image(box)))
        box_res = parse_muffin_annotation(ElementTree.fromstring(requests.get(box_url).content))
        write_iterable_to_file(box_res, c.TEMP_PATH + box.replace(".jpg", "_res.txt"))
        result = result.append(box_res)

    return result

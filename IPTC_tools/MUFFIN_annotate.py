import base64
import requests
from xml.etree import ElementTree
import pandas as pd
import configuration as c

from utils.anotate_utils import prep_boxes, write_iterable_to_file, load_big_image_feedback, parse_muffin_annotation, \
    convert_file_into_dic, parse_class, load_resize_image
from utils.object_detection_utils import load_img



def muffin_annotate(path):
    big_image_url = c.URL_WITH_PARAMS + "&keywords=" + load_big_image_feedback() + "&url=data:image/jpeg;base64," + str(
        base64.b64encode(
            load_resize_image(path)))
    tmp1 = str(base64.b64encode(
        load_resize_image(path)))
    tmp = requests.get(big_image_url).content
    big_image = parse_muffin_annotation(ElementTree.fromstring(requests.get(big_image_url).content))
    write_iterable_to_file(big_image, c.TEMP_PATH + "big_image_keywords.txt")

    C_dic = convert_file_into_dic(c.TEMP_PATH + "C_results.txt")
    OD_dic = convert_file_into_dic(c.TEMP_PATH + "OD_results.txt")
    boxes = prep_boxes()
    result = pd.DataFrame(big_image)

    for box in boxes:
        fed = [parse_class(C_dic[box]), parse_class(OD_dic[box])]
        box_url = c.URL_WITH_PARAMS + "&keywords=" + fed + "url=data:image/jpeg;base64," + str(base64.b64encode(
            load_resize_image(box)))
        box_res = parse_muffin_annotation(ElementTree.fromstring(requests.get(box_url).content))
        write_iterable_to_file(box_res, c.TEMP_PATH + box.replace(".jpg", "_res.txt"))
        result = result.append(box_res)

    return result

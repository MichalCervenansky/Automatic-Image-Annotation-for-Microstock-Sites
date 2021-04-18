import os
import time

import requests
from xml.etree import ElementTree
import pandas as pd
import configuration as c
import unicodedata
from utils.anotate_utils import prep_boxes, write_iterable_to_file, load_big_image_feedback, parse_mufin_annotation, \
    convert_file_into_dic, resize_as_binary_image


def update_in_alist(alist):
    newlist = []
    for (k, v) in alist:
        newlist.append([unicodedata.normalize('NFKD', k).encode('ascii', 'ignore').decode("utf8"), v])
    return newlist


def get_mufin_anotation(image, C_dic, OD_dic):
    tmp_image = resize_as_binary_image(image)
    with open(tmp_image, "rb") as f:
        opened_binary_file = f.read()
        if "boxes_" in image:
            fed_list = []
            if c.USE_OD:
                fed_list += OD_dic[os.path.basename(image)]
            if c.USE_CL:
                fed_list += C_dic[os.path.basename(image)]
            fed = ' '.join([str(elem) for elem in fed_list])
        else:
            fed = load_big_image_feedback()
        box_url = c.URL_WITH_PARAMS
        if fed:
            box_url += "&keywords=" + fed
        req_response = requests.get(box_url, data=opened_binary_file)
        while req_response.status_code != 200:
            req_response = requests.get(box_url, data=opened_binary_file)
            print("Connection to Mufin failed!")
            time.sleep(5)
        img_res = parse_mufin_annotation(
            ElementTree.fromstring(req_response.content))
        img_res = update_in_alist(img_res)
        write_iterable_to_file(img_res, c.TEMP_PATH + os.path.basename(image).replace(".jpg", "_res.txt"))
        res_df = pd.DataFrame(img_res, columns=['Keyword', 'Distance'])
        return res_df


def mufin_annotate(path):
    C_dic, OD_dic = {}, {}
    if c.USE_OD:
        OD_dic = convert_file_into_dic(c.TEMP_PATH + "OD_results.txt")
    if c.USE_CL:
        C_dic = convert_file_into_dic(c.TEMP_PATH + "C_results.txt")
    images = prep_boxes()
    images.append(path)
    result = pd.DataFrame(columns=['Keyword', 'Distance'])

    for image in images:
        res_df = get_mufin_anotation(image, C_dic, OD_dic)
        result = result.append(res_df)

    result = result.groupby(['Keyword']).min()
    result = result.sort_values(by=['Distance'])
    return result.index.values.tolist()

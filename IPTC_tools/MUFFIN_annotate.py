import requests
from xml.etree import ElementTree

ANNOTATOR_URL = "http://disa.fi.muni.cz/anfb/v2/annotate?url="
IMG_URL_BASE = "http://michal.cervenansky.eu/dt_dataset/img_"
K = 50
SIMILAR_IMAGES = 50


def generate_img_url(i):
    if i < 10:
        return IMG_URL_BASE + "0" + str(i) + ".jpg"
    return IMG_URL_BASE + str(i) + ".jpg"


def get_all_gdrive_urls():
    url_list = []
    for i in range(1, 1001):
        url_list.append(ANNOTATOR_URL + generate_img_url(i) + "&k=" + str(K) + "&similarImages=" + str(
            SIMILAR_IMAGES) + "&keywords=")
    return url_list


def muffin_annotate(url, keywords):
    keyword_string = ",".join(keywords)
    response = requests.get(url + keyword_string)
    data = ElementTree.fromstring(response.content)
    return data

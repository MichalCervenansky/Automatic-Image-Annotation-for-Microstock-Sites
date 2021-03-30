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


def parse_muffin_annotation(data):
    res_list = list()
    for word in list(list(data)[0]):
        res_list.append(word.attrib['value'])
    return res_list


def muffin_annotate(url, keywords):
    response = requests.get(url + keywords)
    data = ElementTree.fromstring(response.content)
    result = parse_muffin_annotation(data)
    return result


# 'http://disa.fi.muni.cz/anfb/v2/annotate?k=50&similarImages=1000&url=http://michal.cervenansky.eu/dt_dataset/img_206.jpg&keywords=Clothing,poll parrot,poll,contour feather,street,couple,indigo,Parrot,Man,lory,macaw,parrot,shop,turkish,pet shop'

import sys

import requests
from xml.etree import ElementTree

ANNOTATOR_URL = "http://disa.fi.muni.cz/anfb/v2/annotate?url="
IMG_URL_BASE = "http://michal.cervenansky.eu/dt_dataset/img_"
K = 50
SIMILAR_IMAGES = 50


# Not implemented yet KEYWORDS = set()


def generate_img_url(i):
    if i < 10:
        return IMG_URL_BASE + "0" + str(i) + ".jpg"
    return IMG_URL_BASE + str(i) + ".jpg"

def get_all_gdrive_urls():
    url_list = []
    for i in range(1, 1001):
        url_list.append(ANNOTATOR_URL + generate_img_url(i) + "&k=" + str(K) + "&similarImages=" + str(
            SIMILAR_IMAGES) + "&keywords=")

if __name__ == '__main__':
    output_filename = "keywords"
    if len(sys.argv) > 1:
        output_filename = sys.argv[1]
    f = open(output_filename, "w")
    for i in range(1, 1001):
        print(i)
        url = ANNOTATOR_URL + generate_img_url(i) + "&k=" + str(K) + "&similarImages=" + str(
            SIMILAR_IMAGES) + "&keywords="
        response = requests.get(url)
        data = ElementTree.fromstring(response.content)

        if i < 10:
            filename = "img_" + "0" + str(i) + ".jpg"
        filename = "img_" + str(i) + ".jpg"
        stringBuilder = filename + ":"
        words = list(list(data)[0])
        for word in words:
            stringBuilder += word.attrib['value'] + ";"
        stringBuilder += "\n"
        f.write(stringBuilder)

    f.close()

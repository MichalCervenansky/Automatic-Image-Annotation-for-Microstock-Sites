from PIL import Image
from IPTC_tools.dictionary_manipulation import write_dic
from Positive_feedback.load_from_image import PF_from_IPTC
from Positive_feedback.object_detection import run_detector
from Positive_feedback.image_classification import clasify
import tkinter as tk
from tkinter import filedialog
import os
import configuration as c


def write_iterable_to_file(iterable, filename):
    with open(filename, 'w') as f:
        for item in iterable:
            try:
                f.write("%s" % item)
            except TypeError:
                for each in item:
                    f.write("%s;" % each)
            f.write("\n")


# Opens a dialog to choose input, user can choose multiple images
def pop_up():
    root = tk.Tk()
    root.withdraw()
    return list(filedialog.askopenfilenames(title="Choose files to annotate", initialdir=c.INITIALDIR))


def prep_boxes():
    boxes = []
    for filename in os.listdir(c.TEMP_PATH):
        if filename.startswith("boxes") and filename.endswith(".jpg"):
            boxes.append(c.TEMP_PATH + filename)
    return boxes


def unique(sequence):
    seen = dict.fromkeys(sequence)
    return list(seen.keys())


def add_to_list(list, element):
    list.append(element)
    return list


def process_keywords(iterable):
    return unique(list(map(str.lower, iterable)))


def build_PF(path_to_image, OD_module, C_module):
    positive_feedback = {}
    result_list = []
    if c.USE_IPTC:
        res = process_keywords(PF_from_IPTC(path_to_image))
        positive_feedback["from_image_IPTC"] = res
        result_list += res
    if c.USE_OD:
        res = process_keywords(run_detector(path_to_image, OD_module))
        positive_feedback["from_object_detection"] = res
        result_list += res
    if c.USE_CL:
        res = process_keywords(
            clasify(add_to_list(prep_boxes(), path_to_image), C_module))
        positive_feedback["from_image_classification"] = res
        result_list += res

    result_list = unique(result_list)
    write_dic(positive_feedback, c.TEMP_PATH + "pos_fed_result_dic.txt")
    return result_list


def parse_muffin_annotation(data):
    res_list = list()
    for word in list(list(data)[0]):
        res_list.append((word.attrib['value'], word.attrib['distance']))
    return res_list


def load_big_image_feedback():
    with open(c.TEMP_PATH + "pos_fed_result.txt", 'r') as file:
        fed = file.read().replace('\n', ';')
    return fed[:-1]


def convert_file_into_dic(path):
    dic = {}
    with open(path) as f:
        for line in f.readlines():
            split_line = line.split(";")
            dic[split_line[0]] = []
            if len(split_line) > 2:
                for i in range(1, len(split_line)):
                    split_list = split_line[i].split(":")[0].split(",")
                    flat_list = split_list
                    if "\n" in flat_list: flat_list.remove("\n")
                    dic[split_line[0]] += flat_list
    return dic


def parse_class(key_list):
    class_list = []
    for i in range(len(key_list), step=2):
        class_list.append(key_list[i])
    return class_list


def resize_as_binary_image(path):
    image = Image.open(path).resize((224, 224))
    image.save(c.TEMP_PATH + "small_" + os.path.basename(path))
    return c.TEMP_PATH + "small_" + os.path.basename(path)

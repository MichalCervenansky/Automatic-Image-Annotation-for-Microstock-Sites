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
            f.write("%s\n" % item)


# Opens a dialog to choose input, user can choose multiple images
def pop_up():
    root = tk.Tk()
    root.withdraw()
    return list(filedialog.askopenfilenames(title="Choose files to annotate", initialdir=c.INITIALDIR))


def prep_boxes_for_c():
    boxes = []
    for filename in os.listdir(c.TEMP_PATH):
        if filename.startswith("boxes"):
            boxes.append(c.TEMP_PATH + filename)
    return boxes


def unique(sequence):
    seen = set()
    return [x for x in sequence if not (x in seen or seen.add(x))]


def add_to_list(list, element):
    list.append(element)
    return list


def process_keywords(iterable):
    return unique(list(map(str.lower, iterable)))


def build_PF(path_to_image, OD_module, C_module):
    # return tuples imgname, keyword
    positive_feedback = {"from_image_IPTC": process_keywords(PF_from_IPTC(path_to_image)),
                         "from_object_detection": process_keywords(run_detector(path_to_image, OD_module)),
                         "from_image_classification": process_keywords(clasify(add_to_list(prep_boxes_for_c(), path_to_image), C_module))
                         }
    write_dic(positive_feedback, c.TEMP_PATH + "pos_fed_result_dic.txt")
    result_list = positive_feedback["from_image_IPTC"] + positive_feedback["from_object_detection"] + positive_feedback[
        "from_image_classification"]
    result_list = unique(result_list)
    return result_list

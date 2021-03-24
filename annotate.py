import os
import sys
import tkinter as tk
from tkinter import filedialog
import tensorflow_hub as hub

import config as c
from Positive_feedback.load_from_image import PF_from_IPTC
from Positive_feedback.object_detection import run_detector
from Positive_feedback.image_classification import clasify

"""Opens a dialog to choose input, user can choose multiple images"""


def pop_up():
    root = tk.Tk()
    root.withdraw()
    return list(filedialog.askopenfilenames(title="Choose files to annotate", initialdir=c.INITIALDIR))


def build_PF(path_to_image, OD_module, C_module):
    from_image_IPTC = PF_from_IPTC(path_to_image)
    from_object_detection = run_detector(path_to_image, OD_module)
    images = [path_to_image]
    for filename in os.listdir(c.TEMP_PATH):
        if filename.startswith("boxes"):
            images.append(c.TEMP_PATH + filename)
    from_image_classification = clasify(images, C_module)

    result_set = set(from_image_IPTC + from_object_detection + from_image_classification)
    return result_set


def write_list_to_file(my_list, filename):
    with open(filename, 'w') as f:
        for item in my_list:
            f.write("%s\n" % item)


if __name__ == '__main__':
    if c.POPUP or len(sys.argv) == 1:
        input_path = pop_up()
    else:
        input_path = sys.argv[1:]

        print("loading OD")
        OD_module = hub.load(c.OD_PATH).signatures['default']
        print("loaded!")

        # Load model into KerasLayer
        print("loading classifier")
        C_module = hub.KerasLayer(c.C_PATH)
        print("loaded!")

    for path in input_path:
        pos_feedback = build_PF(path, OD_module, C_module)
        write_list_to_file(pos_feedback, c.TEMP_PATH + "result.txt")

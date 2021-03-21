import sys
import tkinter as tk
from tkinter import filedialog

import config as c
from Positive_feedback.load_from_image import PF_from_IPTC
from Positive_feedback.object_detection import run_detector

"""Opens a dialog to choose input, user can choose multiple images"""


def pop_up():
    root = tk.Tk()
    root.withdraw()
    return list(filedialog.askopenfilenames(title="Choose files to annotate", initialdir=c.INITIALDIR))


def build_PF(path_to_image):
    from_image_IPTC = PF_from_IPTC(path_to_image)
    from_object_detection = run_detector(c.OD_PATH, path_to_image)
    print()


if __name__ == '__main__':
    if c.POPUP or len(sys.argv) == 1:
        input_path = pop_up()
    else:
        input_path = sys.argv[1:]
    build_PF(input_path[0])
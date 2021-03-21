import sys
import tkinter as tk
from tkinter import filedialog

import config as c


def pop_up():
    root = tk.Tk()
    root.withdraw()
    return list(filedialog.askopenfilenames(title="Choose files to annotate", initialdir=c.INITIALDIR))


if __name__ == '__main__':
    print(len(sys.argv))
    if c.POPUP or len(sys.argv) == 1:
        input_path = pop_up()
        print(input_path)

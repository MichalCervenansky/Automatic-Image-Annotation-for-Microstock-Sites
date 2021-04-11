import os
import shutil
import sys

import tensorflow_hub as hub

import configuration as c
from IPTC_tools.IPTC_manipulation import save_iterable_to_IPTC
from utils.MUFIN_annotate import mufin_annotate
from utils.anotate_utils import pop_up, build_PF, write_iterable_to_file


def merge_keywords(pos_feedback, muffin_result):
    merge_res = dict.fromkeys([])
    for each in list(pos_feedback + muffin_result):
        merge_res[each] = None
        if len(merge_res.keys()) == c.MAX_KEYWORDS:
            return merge_res.keys()
    return merge_res.keys()


if __name__ == '__main__':
    if len(sys.argv) == 1:
        input_path = pop_up()
    else:
        input_path = sys.argv[1:]

    if len(input_path) == 0:
        raise ValueError('No input')

    print("loading OD module")
    OD_module = hub.load(c.OD_PATH).signatures['default']
    print("OD module loaded!")

    print("loading classifier module")
    C_module = hub.KerasLayer(c.C_PATH)
    print("classifier module loaded!")

    for path in input_path:
        print("Annotating " + os.path.basename(path))
        pos_feedback = build_PF(path, OD_module, C_module)
        write_iterable_to_file(pos_feedback, c.TEMP_PATH + "pos_fed_result.txt")
        muffin_result = mufin_annotate(path)
        write_iterable_to_file(muffin_result, c.TEMP_PATH + "mufin_result.txt")
        result = merge_keywords(pos_feedback, muffin_result)
        write_iterable_to_file(result, c.TEMP_PATH + "merged_result.txt")
        save_iterable_to_IPTC(result, path)
    if not c.DEBUG:
        shutil.rmtree(c.TEMP_PATH)

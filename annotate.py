import os
import shutil

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
    return list(merge_res.keys())


def annot(input_path):
    OD_module, C_module = None, None
    if os.path.exists(c.TEMP_PATH):
        shutil.rmtree(c.TEMP_PATH)
    os.mkdir(c.TEMP_PATH)

    if c.USE_OD:
        print("loading OD module")
        OD_module = hub.load(c.OD_PATH).signatures['default']
        print("OD module loaded!")

    if c.USE_CL:
        print("loading classifier module")
        C_module = hub.KerasLayer(c.C_PATH)
        print("classifier module loaded!")

    for path in input_path:
        if os.path.exists(c.TEMP_PATH):
            shutil.rmtree(c.TEMP_PATH)
        os.mkdir(c.TEMP_PATH)
        os.mkdir("test_results/" + path)
        print("Annotating " + os.path.basename(path))
        pos_feedback = build_PF(path, OD_module, C_module)
        write_iterable_to_file(pos_feedback, c.TEMP_PATH + "pos_fed_result.txt")
        muffin_result = mufin_annotate(path)
        write_iterable_to_file(muffin_result, c.TEMP_PATH + "mufin_result.txt")
        result = merge_keywords(pos_feedback, muffin_result)
        write_iterable_to_file(result, c.TEMP_PATH + "merged_result.txt")
        save_iterable_to_IPTC(result, path)

        shutil.copyfile(c.TEMP_PATH + "C_results.txt", "test_results/" + path + "C_results.txt")
        shutil.copyfile(c.TEMP_PATH + "OD_results.txt", "test_results/" + path + "OD_results.txt")
        shutil.copyfile(c.TEMP_PATH + "mufin_result.txt", "test_results/" + path + "mufin_result.txt")
        shutil.copyfile(c.TEMP_PATH + "pos_fed_result_dic.txt" + path + "pos_fed_result_dic.txt")
        if not c.DEBUG:
            shutil.rmtree(c.TEMP_PATH)

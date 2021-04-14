import os
import os.path
import subprocess
from os import path

from IPTC_tools.IPTC_manipulation import read_from_IPTC, wipe_keywords
from IPTC_tools.dictionary_manipulation import write_dic

import configuration as c


def prepare_test_result(input_path, output_filename):
    if not path.exists("test_results"):
        os.mkdir("test_results")
    result_dic = dict()
    for image in input_path:
        result_dic[image] = read_from_IPTC(image)

    write_dic(result_dic, "test_results/" + output_filename)


def run_test(suffix):
    input_path = ["/home/mcervenansky/Documents/DP_work/" + filename for filename in
                  os.listdir("/home/mcervenansky/Documents/DP_work/")]
    for each in input_path:
        wipe_keywords(each)
    input_string = "python annotate.py " + " ".join(input_path)
    subprocess.call(input_string, shell=True)
    prepare_test_result(input_path, "test_results_" + suffix + ".txt")


if __name__ == '__main__':
    """Only Muffin"""
    c.USE_IPTC = False
    c.USE_OD = False
    c.USE_CL = False
    run_test("only_muffin")

    """From name"""
    c.USE_IPTC = True
    c.USE_OD = False
    c.USE_CL = False
    run_test("name")

    """From name and OD"""
    c.USE_IPTC = True
    c.USE_OD = True
    c.USE_CL = False
    run_test("OD")

    """From name, OD, CL"""
    c.USE_IPTC = True
    c.USE_OD = True
    c.USE_CL = True
    run_test("CL")
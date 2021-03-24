import sys

import tensorflow_hub as hub

import configuration as c
from IPTC_tools.MUFFIN_annotate import muffin_annotate
from utils.anotate_utils import pop_up, build_PF, write_list_to_file

if __name__ == '__main__':
    if c.POPUP or len(sys.argv) == 1:
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
        pos_feedback = build_PF(path, OD_module, C_module)
        write_list_to_file(pos_feedback, c.TEMP_PATH + "result.txt")
        keyword_string = ",".join(pos_feedback)
        url = "http://disa.fi.muni.cz/anfb/v2/annotate?k=50&similarImages=1000&url=http://michal.cervenansky.eu/dt_dataset/img_206.jpg&keywords="
        tmp = muffin_annotate(url, keyword_string)
        print()


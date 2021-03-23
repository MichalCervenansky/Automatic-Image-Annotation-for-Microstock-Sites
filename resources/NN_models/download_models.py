"""
Download NN models from TensorFlow Hub. Might take a while.
"""

import wget
import os
import shutil
import config as c

"""
Downloads model, unzips it and deletes archive
"""


def download_model(link, path_to_save):
    zip_path = path_to_save + ".tar.gz"
    if not os.path.exists(path_to_save):
        if not os.path.exists(zip_path):
            wget.download(link, zip_path)
        shutil.unpack_archive(zip_path, path_to_save)
        os.remove(zip_path)


openimages_v4_inception_resnet_v2 = "https://tfhub.dev/google/faster_rcnn/openimages_v4/inception_resnet_v2/1?tf-hub" \
                                    "-format=compressed "
download_model(openimages_v4_inception_resnet_v2, c.OD_PATH)

ImageNet_21k_BiT_M = "https://tfhub.dev/google/bit/m-r152x4/imagenet21k_classification/1?tf-hub-format=compressed"
download_model(ImageNet_21k_BiT_M, c.C_PATH)

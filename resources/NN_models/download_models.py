"""""
Download NN models from TensorFlow Hub. Might take a while.
"""""

import wget
import os.path

openimages_v4_inception_resnet_v2 = "https://tfhub.dev/google/faster_rcnn/openimages_v4/inception_resnet_v2/1?tf-hub" \
                                    "-format=compressed "
if not os.path.exists("resources/NN_models/openimages_v4_inception_resnet_v2.tar.gz"):
    wget.download(openimages_v4_inception_resnet_v2, "resources/NN_models/openimages_v4_inception_resnet_v2.tar.gz")

ImageNet_21k_BiT_M = "https://tfhub.dev/google/bit/m-r152x4/imagenet21k_classification/1?tf-hub-format=compressed "
if not os.path.exists("resources/NN_models/ImageNet_21k_BiT_M.tar.gz"):
    wget.download(ImageNet_21k_BiT_M, "resources/NN_models/ImageNet_21k_BiT_M.tar.gz")

import os

import tensorflow as tf
from utils.img2tensor import convert_image
import pandas as pd
import configuration as c


def clasify(images, module):
    images = convert_image(images)  # A batch of images with shape [batch_size, height, width, 3].
    logits = module(images)  # Logits with shape [batch_size, 21843].
    probabilities = tf.nn.softmax(logits)
    classes = open(os.path.join("resources", "NN_models", "imagenet21k_wordnet_lemmas.txt"), "r").readlines()

    data = dict()
    data["Class"] = classes
    data["Probability"] = probabilities
    res_list = []
    for dim in probabilities:
        data["Probability"] = dim
        df = pd.DataFrame(data)
        df = df.sort_values(by=['Probability'], ascending=False).head(c.C_MAX_CLASSES)
        df = df[df["Probability"] >= c.C_PRECISION_THRESHOLD]
        res_list += [x.strip() for x in (df["Class"].tolist())]

    res_classes = [x.strip().split(',') for x in res_list]
    flat_list = [item for sublist in res_classes for item in sublist]
    return list(flat_list)

import os

import tensorflow as tf

from utils.img2tensor import convert_image
import pandas as pd
import configuration as c


def write_C_results(f, path, df):
    f.write(os.path.basename(path) + ";")
    for index, row in df.iterrows():
        f.write(row['Class'].rstrip() + ":" + str(row['Probability']) + ";")
    f.write("\n")


def clasify(images, module):
    converted_images = convert_image(images)  # A batch of images with shape [batch_size, height, width, 3].
    logits = module(converted_images)  # Logits with shape [batch_size, 21843].
    probabilities = tf.nn.softmax(logits)
    classes = open(os.path.join("resources", "NN_models", "imagenet21k_wordnet_lemmas.txt"), "r").readlines()

    data = dict()
    data["Class"] = classes
    data["Probability"] = probabilities
    res_list = []
    f = open(c.TEMP_PATH + "C_results.txt", "w")
    for i in range(len(probabilities)):
        data["Probability"] = probabilities[i]
        df = pd.DataFrame(data)
        df = df.sort_values(by=['Probability'], ascending=False).head(c.C_MAX_CLASSES)
        df = df[df["Probability"] >= c.C_PRECISION_THRESHOLD]
        tmp_list = [x.strip() for x in (df["Class"].tolist())]
        res_list += tmp_list
        write_C_results(f, images[i], df)

    res_classes = [x.strip().split(',') for x in res_list]
    flat_list = [item for sublist in res_classes for item in sublist]
    f.close()
    return list(flat_list)

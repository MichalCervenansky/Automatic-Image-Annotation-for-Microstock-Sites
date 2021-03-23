import tensorflow as tf
import tensorflow_hub as hub
from Positive_feedback.utils.img2tensor import convert_image
import pandas as pd
import config as c


def clasify(images):
    # Load model into KerasLayer
    module = hub.KerasLayer(c.C_PATH)

    images = convert_image(images)  # A batch of images with shape [batch_size, height, width, 3].
    logits = module(images)  # Logits with shape [batch_size, 21843].
    probabilities = tf.nn.softmax(logits)
    classes = open("resources/NN_models/imagenet21k_wordnet_lemmas.txt", "r").readlines()

    data = dict()
    data["Class"] = classes
    data["Probability"] = probabilities
    res_list = []
    for dim in probabilities:
        data["Probability"] = dim
        df = pd.DataFrame(data)
        df = df.sort_values(by=['Probability'], ascending=False).head(c.C_MAX_CLASSES)
        df = df[df["Probability"] >= c.C_PRECISION_THRESHOLD]
        res_list += (df["Class"].tolist())

    res_classes = [x.strip().split(',') for x in res_list]
    return res_classes

"""Configuration"""
import os
import warnings

"""There might be some warnings, that are not important"""
warnings.filterwarnings("ignore")

"""When enabled, app leaves a temp folder in pwd of annotate script and intermediate results are stored there"""
DEBUG = False
TEMP_PATH = "tmp" + os.path.sep
"""Opens a dialog window to choose the input"""
INITIALDIR = ""

"""Sets if keywords and caption from IPTC of image should be used to improve keyword relevancy"""
USE_IPTC = True

"""Settings for Object detection"""
USE_OD = True

OD_PATH = os.path.join("resources", "NN_models", "openimages_v4_inception_resnet_v2")
OD_MAX_BOXES = 5
OD_PRECISION_THRESHOLD = 0.5

"""Settings for Classification"""
USE_CL = True

C_PATH = os.path.join("resources", "NN_models", "ImageNet_21k_BiT_M")
C_MAX_CLASSES = 5
C_PRECISION_THRESHOLD = 0.2

"""Settings for MUFIN Anotation"""
ANNOTATOR_URL = "http://disa.fi.muni.cz/anfb/v2/annotate?"
K = 50
SIMILAR_IMAGES = 115

"""Add &keywords=k1;k2 and &url=SomeLinkOrBinaryImage"""
URL_WITH_PARAMS = ANNOTATOR_URL + "k=" + str(K) + "&similarImages=" + str(SIMILAR_IMAGES)
MAX_KEYWORDS = 50

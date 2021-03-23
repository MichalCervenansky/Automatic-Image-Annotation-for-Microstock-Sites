"""Configuration"""

"""When enabled, app leaves a temp folder in pwd of annotate script and intermediate results are stored there"""
DEBUG = True
TEMP_PATH = "tmp/"

"""Opens a dialog window to choose the input"""
POPUP = False
INITIALDIR = "/home/mcervenansky/Documents/DP_fotky/zmensene"

"""Settings for Object detection"""
OD_PATH = "resources/NN_models/openimages_v4_inception_resnet_v2"
OD_MAX_BOXES = 10
OD_PRECISION_THRESHOLD = 0.3

"""Settings for Classification"""
C_PATH = "resources/NN_models/ImageNet_21k_BiT_M"
C_MAX_CLASSES = 10
C_PRECISION_THRESHOLD = 0.1

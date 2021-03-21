"""Configuration"""

"""When enabled, app leaves a temp folder in pwd of annotate script and intermediate results are stored there"""
DEBUG = True

"""Opens a dialog window to choose the input"""
POPUP = False
INITIALDIR = "/home/mcervenansky/Documents/DP_fotky/zmensene"

"""Settings for Object detection"""
OD_PATH = "resources/NN_models/openimages_v4_inception_resnet_v2"
TEMP_PATH = "tmp/"
OD_MAX_BOXES = 10
OD_PRECISION_THRESHOLD = 0.3

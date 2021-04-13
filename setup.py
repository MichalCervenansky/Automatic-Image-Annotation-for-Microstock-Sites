"""
I would encourage to use some sort of virtual environment, f.e. venv in Pycharm IDE.
Prerequisites and models can have up to 6 GB.
"""
import subprocess
import os

subprocess.call("pip install --upgrade -r requirements.txt", shell=True)

"""
Download NN models from TensorFlow Hub. Might take a while.
"""
download_script_path = os.path.join("resources", "NN_models", "download_models.py")
subprocess.call("python " + download_script_path, shell=True)

import nltk

nltk.download('stopwords')

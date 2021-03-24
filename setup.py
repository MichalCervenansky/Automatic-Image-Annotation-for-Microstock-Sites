"""
Firstly lets install pipenv and create virtual environment
"""
import subprocess
import os

subprocess.call("pip install pipenv", shell=True)
subprocess.call("pipenv install", shell=True)

"""
Download NN models from TensorFlow Hub. Might take a while.
"""
download_script_path = os.path.join("resources", "NN_models", "download_models.py")
subprocess.call("pipenv run python " + download_script_path, shell=True)

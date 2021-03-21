"""""
Firstly lets install pipenv and create virtual environment 
"""""
import subprocess

subprocess.call(["pip", "install", "pipenv"])
subprocess.call(["pipenv", "install"])

"""""
Download NN models from TensorFlow Hub. Might take a while.
"""""
subprocess.call(["pipenv", "run", "python", "resources/NN_models/download_models.py"])

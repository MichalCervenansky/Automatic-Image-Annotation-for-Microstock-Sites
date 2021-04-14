# Automatic image annotation for microstock sites
Application serves for automatic image annotation, mainly for microstock websites like Shutterstock, Fotolia,... It is using several approaches, which can be combined and set in config.py:
* Collecting keyword from IPTC of image and parsing keywords from a caption in IPTC of image
* Detecting objects on the image using Object detection module inception_resnet_v2 trained on OpenImagesV4
* Classification by BiT-M model trained on ImageNet-21k of image itself and objects detected in previous step
* Completing keywords using Mufin annotation framework with positive feedback from previous steps

## Instalation:
* Clone or download this repository from Github
* Install Python and pip, tested with Python 3.6 and 3.7 other version might cause problems
* Activating virtual environment is recommended, prerequisites might have up to 6 GB, tested using venv in Pycharm IDE.
* Run `setup.py`, this will install `requirements.txt` as well as download NN models and wordnet stopwords.
* Mainly on Windows there might be problem with Tensorflow installation, if this occurs make sure to follow:
https://www.tensorflow.org/install/pip
  
## Workflow:
* Run `annotate.py` from terminal with images as parameters for example:\
`python annotate.py /path/*.jpg` \
  `python annotate.py /path/01.jpg /path/02.jpg`
  * Run `annotate.py` without any parameter and select images in the pop-up window
  * Results of annotation are automatically saved to IPTC of annotated images. 
  * Feel free to experiment with application parameters in `configuration.py` file

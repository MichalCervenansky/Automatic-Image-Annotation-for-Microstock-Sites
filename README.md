# Automatic Image Annotation for Microstock Sites
Application serves for automatic image annotation, mainly for microstock websites like Shutterstock, Fotolia,... It is using several approaches, which can be combined and set-up in config.py:
* Collecting keyword from IPTC of image and parsing keywords from the caption in IPTC metadata of the image
* Detecting objects on the image using Object detection module [inception_resnet_v2 trained on OpenImagesV4 dataset](https://tfhub.dev/google/faster_rcnn/openimages_v4/inception_resnet_v2/1)
* Classification by [BiT-M model trained on ImageNet-21k](https://tfhub.dev/google/bit/m-r152x4/imagenet21k_classification/1) of image itself and objects detected in previous step
* Completing keywords using [MUFIN annotation framework](http://disa.fi.muni.cz/demo/image-annotation/) with using keywords from previous steps as seed keywords to improve results

![alt text](https://github.com/MichalCervenansky/Automatic-image-annotation-for-microstock-sites/blob/main/diagram.png?raw=true "Annotation pipeline diagram. Blue color represents data elements and red represents processes or methods")

## Instalation:
* Clone or download this repository from Github
* Install [Python](https://www.python.org/) and [pip](https://pypi.org/project/pip/), tested with Python 3.6 and 3.7 other version might cause problems
* Activating virtual environment is recommended, prerequisites might have up to 6 GB, tested using venv in Pycharm IDE.
* Run `setup.py`, this will install `requirements.txt` as well as download NN models and wordnet stopwords.
* Mainly on Windows there might be problem with Tensorflow installation, if this occurs make sure to follow [this guide](https://www.tensorflow.org/install/pip).
* Rename the cloned repository if it is necessary due to "Destination Path Too Long" error.

  
## Workflow:
* Run `annotate.py` from terminal or using IDE with images as parameters for example:\
`python annotate.py /path/*.jpg` \
`python annotate.py /path/01.jpg /path/02.jpg`
* Run `annotate.py` without any parameter and select images in the pop-up window
* Results of annotation are automatically saved to IPTC of annotated images. 
* Feel free to experiment with application parameters in `configuration.py` file

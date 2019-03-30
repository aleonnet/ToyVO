import numpy as np
import cv2
import yaml

class ConfigLoader(object):
    """Class that loads yaml configurations for objects"""

    def __init__(self):
        pass

class ImageLoader(object):
    """Class that returns images from a dataset

    Attributes:
        path (str): Path to the folder containing the images
        database (list[str]): Sorted list of image filenames
    """

    def __init__(self, path = None):
        self.path = path
        self.database = []
    
    def getImage(index = None):
        """Returns index-th image"""
        if index is not None:
            # Warning: will just return None if imread fails
            return(cv2.imread(database[index]))


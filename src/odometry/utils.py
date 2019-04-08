import numpy as np
import cv2
import glob
from enum import Enum

def test_image(image):
    if (len(image.shape) < 3):
        return ImageType.GRAY
    else:
        return ImageType.COLOR

class ImageType(Enum):
    GRAY = 1
    COLOR = 2

class ImageLoader(object):
    """Class that returns images from a dataset

    Attributes:
        path (str): Path to the folder containing the images
        database (list[str]): Sorted list of image filenames
    """

    def __init__(self, path = None):
        self.path = path
        self.database = glob.glob(path + '*.*')
        self.database.sort()
        self.num_images = len(self.database)
        self.color = test_image(cv2.imread(self.database[0]))

    
    def get_image(self, index = None):
        """Returns index-th image"""
        if index is not None:
            # Warning: will just return None if imread fails
            return(cv2.imread(self.database[index]))


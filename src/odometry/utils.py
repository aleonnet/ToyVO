import numpy as np
import cv2
import glob

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
    
    def get_image(self, index = None):
        """Returns index-th image"""
        if index is not None:
            # Warning: will just return None if imread fails
            return(cv2.imread(self.database[index]))


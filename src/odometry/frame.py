import numpy as np
import cv2

class Frame(object):
    """Class representing an image and its tracked feautres

    Attributes:
        image (np.array): Image taken in current frame
    """

    def __init__(self, K = None, pose = None, image=None):
        self.K = K
        self.pose = pose
        self.image = image

        self.features = []
        


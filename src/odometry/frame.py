import numpy as np
import cv2

class Frame(object):
    """Class representing an image and its tracked feautres

    Attributes:
        image (np.array): Image taken in current frame
    """

    def __init__(self, K = None, pose = None, image_color=None, image_gray = None):
        self.K = K
        self.pose = pose
        self.image_color = image_color
        self.image_gray = image_gray

        self.features = []
        


import numpy as np
import cv2

class Frame(object):
    """Class representing an image and its tracked feautres

    Attributes:
        image_gray (np.array): Grayscale image taken in current frame
        image_color (np.array): Color image taken in current frame
        pose (np.array): 4D homogeneous transformation matrix from previous frame to
            current frame coordinates
            Note: To form trajectory, concatenate all transformations 
        features (np.array): Pixel coordinates of features known in this frame
            Note: features of frame n+1 will be fewer than frame n as known features
                can fail to be located in the next frame
    """

    def __init__(self, pose = None, image_color=None, image_gray = None):
        self.pose = pose
        self.image_color = image_color
        self.image_gray = image_gray

        self.features = None

        """ replace features with these when switching over to FREAK+Fast-Hessian
        self.keypoints = None
        self.descriptors = None
        """

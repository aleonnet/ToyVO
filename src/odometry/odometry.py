import numpy as np
import cv2

from enum import Enum

from odometry.camera import Camera
from odometry.utils import ImageLoader, ImageType
from odometry.frame import Frame

class TrackingState(Enum):
    UNINITIALIZED = 1
    TRACKING = 2
    END_OF_IMAGES = 3

class Odometry(object):
    """A class representing a visual odometry system

    Attributes:
        cam (Camera): The camera the VO system uses
        image_loader (ImageLoader): Loader for images

    """
    def __init__(self, camera = None, image_path = None):
        """Inits Odometry with a camera"""
        self.cam = camera if camera is not None else Camera()
        self.image_loader = ImageLoader(image_path)
        self.state = TrackingState.UNINITIALIZED

        self.frames = []
        self.poses = []
        self.next_idx = 0 # index of next image to be processed

        # Lucas-Kanade tracking info
        # https://docs.opencv.org/3.4/d7/d8b/tutorial_py_lucas_kanade.html
        self.lk_params = dict(winSize = (15,15),
                              maxLevel = 2,
                              criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT,
                                        10, 0.03))
        self.feature_params = dict(maxCorners = 100,
                                   qualityLevel = 0.3,
                                   minDistance = 7,
                                   blockSize = 7)

    def initialize_tracking(self):
        """TODO: Docstring and implementation
        Process first two frames, get initial pose estimates, yada yada
        """
        image_0 = self.image_loader.getImage(self.next_idx)
        pose_0 = np.eye(4)
        self.add_frame(self.cam.K, pose_0, image_0)
        # ...
        self.state = TrackingState.TRACKING

    def add_frame(self, image, pose, K):
        # cv2.goodFeaturesToTrack() requires a grayscale image,
        # handle the 
        if self.image_loader.color is ImageType.GRAY:
            new_frame = Frame(K = K,
                              pose = pose,
                              image_gray = image)
        else:
            new_frame = Frame(K = K, 
                              pose = pose,
                              image_color = image)
            new_frame.image_gray = cv2.cvtColor(new_frame.image_color, 
                                                cv2.COLOR_BGR2GRAY)
        new_frame.features = cv2.goodFeaturesToTrack(new_frame.image_gray,
                                                     mask = None,
                                                     **self.feature_params)
        self.frames.append(new_frame)

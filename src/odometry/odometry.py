import numpy as np
import cv2

from enum import Enum

from odometry.camera import Camera
from odometry.utils import ImageLoader
from odometry.frame import Frame

class TrackingState(Enum):
    UNINITIALIZED = 1
    INITIALIZING = 2
    TRACKING_GOOD = 3
    END_OF_IMAGES = 4

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

    def initialize(self):
        """TODO: Docstring"""
        image_0 = self.image_loader.getImage(self.next_idx)
        frame_0 = Frame(image_0)
        pose_0 = np.eye(4)

    def add_frame(self, image):
        new_frame = Frame(current_image)
        self.frames.append(new_frame)

    def process_frame(self):
        """TODO"""
        pass

    def run_odometry(self):
        pass

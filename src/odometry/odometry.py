import numpy as np
import cv2

from odometry.camera import Camera
from odometry.utils import ImageLoader
from odometry.frame import Frame

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
        self.frames = []
        self.poses = []
        self.next_idx = 0 # index of next image to be processed

    def initialize(self):
        """TODO: Docstring"""
        image_0 = self.image_loader.getImage(self.next_idx)
        frame_0 = Frame(image_0)

        pose_0 = np.eye(4)




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
        self.next_idx = 0 # index of next image to be processed
        
        self.min_features = 1000 
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

        # Assume first frame takes place at origin
        image0 = self.image_loader.get_image(self.next_idx)
        pose0 = np.eye(4)

        if self.image_loader.color is ImageType.GRAY:
            initial_frame = Frame(image_gray = image0,
                                  pose = pose0)
        else:
            initial_frame = Frame(image_color = image0,
                                  pose = pose0)
            initial_frame.image_gray = cv2.cvtColor(initial_frame.image_color,
                                                    cv2.COLOR_BGR2GRAY)
        
        initial_frame.features = cv2.goodFeaturesToTrack(initial_frame.image_gray,
                                                     mask = None,
                                                     **self.feature_params)

        self.frames.append(initial_frame)

        self.next_idx = self.next_idx + 1

        # Now process second frame, track features, and calculate pose
        image1 = self.image_loader.get_image(self.next_idx)
        if self.image_loader.color is ImageType.GRAY:
            second_frame = Frame(image_gray = image1)
        else:
            second_frame = Frame(image_color = image1)
            second_frame.image_gray = cv2.cvtColor(second_frame.image_color,
                                                   cv2.COLOR_BGR2GRAY)
        
        # track features
        pts2, st, err = cv2.calcOpticalFlowPyrLK(initial_frame.image_gray,
                                                 second_frame.image_gray,
                                                 initial_frame.features,
                                                 None,
                                                 **self.lk_params)
        # remove failed poins
        second_frame.features = pts2[st == 1]

        # calculate pose
        E, mask = cv2.findEssentialMat(initial_frame.features[st == 1],
                                       second_frame.features,
                                       self.cam.K,
                                       cv2.RANSAC,
                                       threshold = 2,
                                       prob = .99)
        _, R, t, mask = cv2.recoverPose(E,
                                        initial_frame.features[st == 1],
                                        second_frame.features,
                                        self.cam.K)
        pose1 = np.eye(4)
        pose1[0:3, 0:3] = R
        pose1[0:3,3] = np.squeeze(t)
        second_frame.pose = pose1
        self.frames.append(second_frame)
        # ...
        self.next_idx = self.next_idx + 1
        self.state = TrackingState.TRACKING

    def add_frame(self, pose = None, image = None):
        """ Calculate the pose of the camera in a new image and add that state to the system.

        Steps:
            Create a new frame with the image
            Track features from the previous frame into the new frame
            Calculate camera pose
            Append frame to system

        Arguments:
            image (np.array): The image taken at this frame

        Returns:
            None
        """

        # Create new frame
        if self.image_loader.color is ImageType.GRAY:
            new_frame = Frame(image_gray = image)
        else:
            new_frame = Frame(image_color = image)
            new_frame.image_gray = cv2.cvtColor(new_frame.image_color, 
                                                cv2.COLOR_BGR2GRAY)
        
        # Track features into this new frame

        self.frames.append(new_frame)
        self.next_idx = self.next_idx + 1

    
    def run_odometry(self):
        pass

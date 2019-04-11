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
        self.R = None
        self.t = None

        self.frames = []
        self.next_idx = 0 # index of next image to be processed

        self.min_features = 100 # when using a descriptor besides GFTT this should be much higher
        # Lucas-Kanade tracking info
        # https://docs.opencv.org/3.4/d7/d8b/tutorial_py_lucas_kanade.html
        # TODO: Replace goodFeaturesToTrack with surf detector and freak descriptor
        # as suggested here:
        # https://link.springer.com/content/pdf/10.1007%2Fs10846-017-0762-8.pdf
        self.detector = cv2.xfeatures2d.SURF_create() # not used yet
        self.extractor = cv2.xfeatures2d.FREAK_create() # not used yet
        self.matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True) # not used yet
        self.lk_params = dict(winSize = (15,15),
                              maxLevel = 2,
                              criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT,
                                          10, 0.03))
        self.feature_params = dict(maxCorners = 1500,
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
        self.R = np.eye(3)
        self.t = np.zeros((3,1))

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
        # TODO: Look to move this into add_frame maybe
        image1 = self.image_loader.get_image(self.next_idx)
        if self.image_loader.color is ImageType.GRAY:
            second_frame = Frame(image_gray = image1)
        else:
            second_frame = Frame(image_color = image1)
            second_frame.image_gray = cv2.cvtColor(second_frame.image_color,
                                                   cv2.COLOR_BGR2GRAY)

        # track features
        pts1, st, err = cv2.calcOpticalFlowPyrLK(initial_frame.image_gray,
                                                 second_frame.image_gray,
                                                 initial_frame.features,
                                                 None,
                                                 **self.lk_params)

        second_frame.features = pts1[st == 1]
        initial_frame.features = initial_frame.features[st == 1]

        # calculate pose
        E, mask = cv2.findEssentialMat(initial_frame.features,
                                       second_frame.features,
                                       self.cam.K,
                                       cv2.RANSAC,
                                       threshold = 2,
                                       prob = .99)
        _, R, t, mask = cv2.recoverPose(E,
                                        initial_frame.features,
                                        second_frame.features,
                                        self.cam.K)
        print(t.shape)

        self.R = R.dot(self.R)
        self.t = self.t + self.R.dot(t)

        pose1 = np.eye(4)
        pose1[0:3, 0:3] = R
        pose1[0:3,3] = np.squeeze(t)
        second_frame.pose = pose1
        self.frames.append(second_frame)

        self.next_idx = self.next_idx + 1 # ready to read third frame next
        self.state = TrackingState.TRACKING # successful initialization

    def add_frame(self, pose = None, image = None):
        # TODO: NOT FINISHED
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
        print(self.next_idx)
        if image is None:
            self.state = TrackingState.END_OF_IMAGES
            return

        # Access a copy of the previous frame 
        previous_frame = self.frames[self.next_idx - 1]

        # pad features from previous frame for masking
        previous_frame.features = previous_frame.features[:,np.newaxis,:]

        # TODO: Re-detect features if below threshold

        # Create new frame
        if self.image_loader.color is ImageType.GRAY:
            new_frame = Frame(image_gray = image)
        else:
            new_frame = Frame(image_color = image)
            new_frame.image_gray = cv2.cvtColor(new_frame.image_color, 
                                                cv2.COLOR_BGR2GRAY)

        # Check if there are enough features, and redetect if not
        if np.amax(previous_frame.features.shape) <= self.min_features:
            previous_frame.features = cv2.goodFeaturesToTrack(previous_frame.image_gray,
                                                              mask = None,
                                                              **self.feature_params)

        # Track features into this new frame
        pts_new, st, err = cv2.calcOpticalFlowPyrLK(previous_frame.image_gray,
                                                    new_frame.image_gray,
                                                    previous_frame.features,
                                                    None,
                                                    **self.lk_params)

        new_frame.features = pts_new[st == 1]
        previous_frame.features = previous_frame.features[st == 1]

        # calculate pose
        E, mask = cv2.findEssentialMat(previous_frame.features,
                                       new_frame.features,
                                       self.cam.K,
                                       cv2.RANSAC,
                                       threshold = 2,
                                       prob = .99)
        _, R, t, mask = cv2.recoverPose(E,
                                        previous_frame.features,
                                        new_frame.features,
                                        self.cam.K)

        self.R = R.dot(self.R)
        self.t = self.t + self.R.dot(t)
        print(self.t)

        pose1 = np.eye(4)
        pose1[0:3, 0:3] = R
        pose1[0:3,3] = np.squeeze(t)
        new_frame.pose = pose1

        self.frames.append(new_frame)
        self.next_idx = self.next_idx + 1

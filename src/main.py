import numpy as np
import cv2
import yaml

from odometry.camera import Camera
from odometry.odometry import Odometry
from odometry.utils import ConfigLoader

if __name__ == '__main__':
    print("Hello, world!")
    
    config_loader = ConfigLoader()

    cam = Camera()
    odom = Odometry(cam)

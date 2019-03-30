import numpy as np
import cv2
import yaml

from odometry.camera import Camera
from odometry.odometry import Odometry

if __name__ == '__main__':
    print("Hello, world!")
    
    cam = Camera()
    odom = Odometry(cam)

# Math
import numpy as np
import cv2

# Utility Imports
import yaml
import argparse

# Personal files
from odometry.camera import Camera
from odometry.odometry import Odometry

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--camera', help='Location of camera config file', type=str, default='../config/camera.yaml', required=False)
    parser.add_argument('-p', '--path', help='Folder containing images', type=str, default='../data/', required=False)
    args = parser.parse_args()

    with open(args.camera, 'r') as stream:
        try:
            camera_dict = yaml.load(stream, Loader=yaml.BaseLoader)
        except yaml.YAMLError as exc:
            print(exc)

    cam = Camera(camera_dict)
    odom = Odometry(cam, args.path)

# Math
import numpy as np
import cv2

# Utility imports
import yaml
import argparse

# Personal files
from odometry.camera import Camera
from odometry.odometry import Odometry, TrackingState

def initializeOdometry(args):
    """ return odometry system """
    with open(args.camera, 'r') as stream:
        camera_dict = yaml.load(stream, Loader=yaml.BaseLoader)
    cam = Camera(camera_dict)
    odom = Odometry(cam, args.path)
    return odom

def run_odometry(args):
    # TODO: Initialization phase 1
    #   Initialize odometry object
    odom = initializeOdometry(args)
    #   Grab first frame
    #   Detect features
    #   Set state to initializing
    odom.initialize_tracking()
    if odom.state is not TrackingState.TRACKING:
        print("Error in initialization. Exiting")
        return
    
    # TODO: Initialize tracking loop
    for i in range(2, odom.image_loader.num_images):
        # run loop
        pass

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', 
                        '--camera', 
                        help='Location of camera config file', 
                        type=str, default='../config/camera.yaml', 
                        required=False)
    parser.add_argument('-p', 
                        '--path', 
                        help='Folder containing images', 
                        type=str, 
                        default='../data/', 
                        required=False)

    args = parser.parse_args()
    
    run_odometry(args)



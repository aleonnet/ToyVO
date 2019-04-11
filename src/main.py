# Math
import numpy as np
import cv2

# Utility imports
import yaml
import argparse

# Personal files
from odometry.camera import Camera
from odometry.odometry import Odometry, TrackingState

def initialize_odometry(args):
    """ return odometry system """
    with open(args.camera, 'r') as stream:
        camera_dict = yaml.load(stream, Loader=yaml.BaseLoader)
    cam = Camera(camera_dict)
    odom = Odometry(cam, args.path)
    return odom

def run_odometry(args, show_traj = False):
    # TODO: Initialization phase 1
    #   Initialize odometry object
    odom = initialize_odometry(args)
    odom.initialize_tracking()
    if odom.state is not TrackingState.TRACKING:
        print("Error in initialization. Exiting")
        return

    if show_traj is True:
        traj = np.zeros((600, 600, 3), dtype = np.uint8)

    # TODO: Initialize tracking loop
    for i in range(2, odom.image_loader.num_images):
        # run loop
        new_image = odom.image_loader.get_image(i)
        odom.add_frame(image = new_image)
        cv2.imshow("Frame", new_image)

        if show_traj is True:
            x = int(odom.t[0]) + 300
            y = int(odom.t[1]) + 300
            z = int(odom.t[2]) + 300
            cv2.circle(traj, (x, z), 1, (0,0,255), 1)
            cv2.imshow("Trajectory", traj)
        cv2.waitKey(100)

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

    run_odometry(args, show_traj = True)



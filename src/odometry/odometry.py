import numpy as np
import cv2

class Camera:
    """ A class representing a pinhole camera

    Attributes:
        K (np.array): The camera matrix in form [fx 0 cx; 0 fy cy; 0 0 1]
        dist_coeffs (np.array): Distortion coefficients in form [k1 k2 p1 p2 k3]
    """
    def __init__(self, K = None, dist_coeffs = None):
        """ Inits Camera with given camera matrix and distortion coefficients"""
        self.K = K if K is not None else np.zeros((3,3))
        self.dist_coeffs = dist_coeffs if dist_coeffs is not None else np.array([0, 0, 0, 0, 0])

    def undistort(self, image):
        """Takes an image and returns the image undistorted"""
        return False

    def projectPoints(self, points3d):
        """Returns the (u,v) pixel coordinates of 3d points in camera reference frame projected onto the image plane"""
        return False
    

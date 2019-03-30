import numpy as np
import cv2

class Camera(object):
    """ A class representing a pinhole camera

    Attributes:
        K (np.array): The camera matrix in form [fx 0 cx; 0 fy cy; 0 0 1]
        dist_coeffs (np.array): Distortion coefficients in form [k1 k2 p1 p2 k3]
    """
    def __init__(self, camera_dict=None):
        """ Inits Camera with given camera matrix and distortion coefficients

        Args:
            camera_dict (dict{str:list}): Dictionary containing:
                K (dict{str:float}): Dictionary containing:
                    fx
                    fy
                    cx
                    cy
                dist_coeffs (dict{str:float}): Dictionary containing:
                    k1
                    k2
                    p1
                    p2
                    k3
        """
        
        K = camera_dict['K']

        dist_coeffs = camera_dict['dist_coeffs']
        dist_coeffs = np.array([dist_coeffs['k1'], dist_coeffs['k2'], dist_coeffs['p1'], 
                                dist_coeffs['p2'], dist_coeffs['k3']], dtype=np.float32)

        self.K = self.makeCameraMatrix(K) if K is not None else np.zeros((3,3))
        self.dist_coeffs = dist_coeffs if dist_coeffs is not None else np.array([0, 0, 0, 0, 0])

    def undistortImage(self, image):
        """Takes an image and returns the image undistorted

        Args:
            image (np.array): A distorted image (color/black and white?)

        Returns:
            undistorted_image (np.array): The image undistorted
        """
        return False

    def undistortPoints(self, points2d):
        """Takes pixel coordinates from a distorted image and undistortes them

        Args:
            points2d (np.array): Pixel coordinates of points in distorted image

        Returns:
            undistorted_points2d (np.array): Pixel coordinates of points in undistorted image
        """
        return False

    def projectPoints(self, points3d):
        """Projects 3d points onto the image plane.

        Args:
            points3d (np.array): An n-by-3 numpy array of 3d points in the camera frame

        Returns:
            points2d (np.array): An n-by-2 numpy array of pixel coordinates
        """
        return False
    
    def makeCameraMatrix(self, paramDict):
        """Constructs a camera matrix from the given parameters
        
        Args:
            paramDict (dictionary {str : float}): Dictionary containing
                - fx
                - fy
                - cx
                - cy
        
        Returns:
            K (np.array): A 3-by-3 numpy array of form:
                [fx 0 cx]
                [0 fy cy]
                [0 0 1]
        """
        fx = paramDict['fx']
        fy = paramDict['fy']
        cx = paramDict['cx']
        cy = paramDict['cy']
        K = np.array([[fx, 0, cx], 
                      [0, fy, cy], 
                      [0, 0, 1]], dtype=np.float32)
        return K
    

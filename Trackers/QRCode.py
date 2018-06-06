"""
    QR Code detector
    >_ uses open cv to track 
"""

# import the necessary packages
from __future__ import print_function
import pyzbar.pyzbar as pyzbar
import numpy as np
import cv2
import math

from picamera.array import PiRGBArray
from picamera import PiCamera
import imutils


class Tracker:
    '''
        iFollow robot class
    '''

    def __init__(self, password, frameSize=800):
        """
            Args: List of color tuples: [[(0,0,0),(255,255,255)]...]
        """
        self.password = password
        # capturing video through webcam
        self.camera = PiCamera()
        self.rawCapture = PiRGBArray(self.camera)
        self.status = "Running"
        self.cameraWidth = frameSize

    def __str__(self):
        '''
        Object Representation
        '''
        print("Ok!")

    def decode(self, im):
        # Find barcodes and QR codes
        decodedObjects = pyzbar.decode(im)
        return decodedObjects

    def distance(self, a, b):
        dist = math.hypot(b[0] - a[0], b[1] - a[1])
        return dist

    def detectObjects(self, im, decodedObjects):

        # Loop over all decoded objects
        for decodedObject in decodedObjects:
            if decodedObject.data.decode('utf-8') == self.password:
                points = decodedObject.polygon
                sortedPointsX = sorted(points, key=lambda point: point[0])
                sortedPointsY = sorted(points, key=lambda point: point[0])
                center = self.distance(points[1], points[0]) / 2 + \
                    sortedPointsX[0][0], self.distance(
                        points[3], points[2])/2 + sortedPointsX[0][1]
                print(points)
                return center
        return None, None

    def getCenter(self, frame):
        # resize the frame, blur it, and convert it to the HSV
        # color space
        img = imutils.resize(frame, width=600)
        # Converts image to grayscale.
        decodedObjects = self.decode(img)
        center = self.detectObjects(img, decodedObjects)
        # Wait for the magic key
        return center

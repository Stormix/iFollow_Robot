"""
    Color detector
    >_ uses open cv to track a multiple colors as specified
"""

# import the necessary packages
import numpy as np
import sys
import imutils
import cv2
import colorsys
from picamera.array import PiRGBArray
from picamera import PiCamera
import io


class Tracker:
    '''
        iFollow robot class
    '''

    def __init__(self, colors, frameSize):
        """
            Args: List of 2 color tuples: [(0,0,0),(255,255,255)]
        """
        self.colors = colors
        # capturing video through webcam
        self.camera = PiCamera()
        self.rawCapture = PiRGBArray(self.camera)
        self.status = "Running"
        self.minRadius = 20
        self.cameraWidth = frameSize

    def __str__(self):
        '''
        Object Representation
        '''
        print("Ok!")

    def prepareColors(self):
        colors = self.colors
        Min = colors[0]
        Max = colors[1]
        return (np.array(list(Min), np.uint8),
                np.array(list(Max), np.uint8))

    def detectObject(self, mask, frame):
        contours = cv2.findContours(
            mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        if len(contours) > 0:
            c = max(contours, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            # only proceed if the radius meets a minimum size
            if radius > self.minRadius:
                # draw the circle and centroid on the frame,
                # then update the list of tracked points
                cv2.circle(frame, (int(x), int(y)), int(radius),
                           (255, 255, 255), 2)
                cv2.circle(frame, center, 2, (0, 255, 0), -1)
                return x
        return None

    def createMask(self, hsv, frame):
        masks = []
        color = self.prepareColors()
        # finding the range of red,blue and yellow color in the image
        mask = cv2.inRange(hsv, color[0], color[1])
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)
        # Morphological transformation, Dilation
        kernal = np.ones((5, 5), "uint8")
        mask = cv2.dilate(mask, kernal)
        #mask = cv2.bitwise_and(frame, frame, mask = mask)
        return mask

    def getCoordinate(self, blur, frame=np.array([False, False])):
        # keep looping
        # grab the current frame
        if not frame.all():
            stream = io.BytesIO()
            camera = self.camera
            camera.resolution = (400, 400)
            camera.start_preview()
            stream = PiRGBArray(camera)
            camera.capture(stream, format='bgr')
            # At this point the image is available as stream.array
            frame = stream.array
        #image = self.rawCapture.array
        # resize the frame, blur it, and convert it to the HSV color space
        frame = imutils.resize(frame, width=self.cameraWidth)
        frame = cv2.flip(frame, 1)
        blurred = cv2.GaussianBlur(frame, (11, 11), 0) if blur else frame
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
        mask = self.createMask(hsv, frame)
        self.rawCapture.truncate(0)
        # Track each color:
        return self.detectObject(mask, frame)

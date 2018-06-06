"""
    Color detector
    >_ uses open cv to track a multiple colors as specified
"""

# import the necessary packages
import numpy as np
import argparse
import sys
import imutils
import cv2
import colorsys

from picamera.array import PiRGBArray
from picamera import PiCamera
import io
import math


class Tracker:
    '''
        iFollow robot class
    '''

    def __init__(self, colors, frameSize):
        """
            Args: List of color tuples: [[(0,0,0),(255,255,255)]...]
        """
        self.colors = colors
        # capturing video through webcam
        self.camera = PiCamera()
        self.rawCapture = PiRGBArray(self.camera)
        self.status = "Running"
        self.minArea = 300
        self.cameraWidth = frameSize

    def __str__(self):
        '''
        Object Representation
        '''
        print("Ok!")

    def prepareColors(self):
        new_colors = []
        for color in self.colors:
            Min = color[0]
            Max = color[1]
            new_colors += [(np.array(list(Min), np.uint8),
                            np.array(list(Max), np.uint8))]
        return new_colors

    def cleanUpRGB(self, r, g, b):
        r = int(r) if int(r) > 0 else 0
        b = int(b) if int(b) > 0 else 0
        g = int(g) if int(g) > 0 else 0
        return 255, 255, 255

    def createMasks(self, hsv, frame):
        masks = []
        for color in self.prepareColors():
            # finding the range of red,blue and yellow color in the image
            mask = cv2.inRange(hsv, color[0], color[1])
            mask = cv2.erode(mask, None, iterations=2)
            mask = cv2.dilate(mask, None, iterations=2)
            # Morphological transformation, Dilation
            kernal = np.ones((5, 5), "uint8")
            mask = cv2.dilate(mask, kernal)
            #mask = cv2.bitwise_and(frame, frame, mask = mask)
            masks += [(mask, color[0])]
        return masks

    def drawContours(self, maskTuple, frame):
        color = maskTuple[1]
        mask = maskTuple[0]
        color_id = color
        contours = cv2.findContours(
            mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        if len(contours) > 0:
            contour = max(contours, key=cv2.contourArea)
            area = cv2.contourArea(contour)
            if(area > self.minArea):
                #print("Tracking Mask ", str(color))
                hh, s, v = color
                r, g, b = tuple(round(i * 255)
                                for i in colorsys.hsv_to_rgb(hh, s, v))
                x, y, w, h = cv2.boundingRect(contour)
                frame = cv2.rectangle(
                    frame, (x, y), (x+w, y+h), (self.cleanUpRGB(r, g, b)), 2)
                cv2.putText(frame, str((self.cleanUpRGB(r, g, b)))+" color", (x, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (self.cleanUpRGB(r, g, b)))
                return x + w/2, y + h/2

    def capture(self, blur=False, frame=np.array([False, False])):
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
        blurred = cv2.GaussianBlur(frame, (11, 11), 0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
        ranges = []
        masks = self.createMasks(hsv, frame)
        # Track each color:
        rectangles = []
        for mask in masks:
            rectangles += [self.drawContours(mask, frame)]
        if len([r for r in rectangles if r != None]) > 2:
            print(self.getCenter([r for r in rectangles if r != None]))
        cv2.imshow("Color Tracking", frame)
        self.rawCapture.truncate(0)
        # cv2.imshow("red",res)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            cap.release()
            cv2.destroyAllWindows()

    def distance(self, a, b):
        # (x1,y1) (x2,y2)
        if (a != (None, None) and b != (None, None)) and (len(a) > 0 and len(b) > 0):
            dist = math.hypot(b[0] - a[0], b[1] - a[1])
            return dist

    def intersection(self, lst1, lst2):
        return list(set(lst1) & set(lst2))

    def getCenter(self, rectangles):
        # get rectangles on the top
        # they have the same y coordinates
        Rectanglesy = sorted(
            rectangles, key=lambda rectangle: rectangle[1], reverse=True)
        Rectanglesx = sorted(rectangles, key=lambda rectangle: rectangle[1])
        topRectangles = Rectanglesy[:2]
        bottomRectangles = Rectanglesy[2:]
        leftRectangles = Rectanglesy[:2]
        rightRectangles = Rectanglesy[2:]

        upperLeft = self.intersection(topRectangles, leftRectangles)
        upperRight = self.intersection(topRectangles, rightRectangles)
        lowerLeft = self.intersection(bottomRectangles, leftRectangles)
        lowerRight = self.intersection(bottomRectangles, rightRectangles)
        print(upperLeft, upperRight, lowerRight, lowerLeft)
        center = self.distance(upperLeft, upperRight), self.distance(
            upperLeft, lowerLeft)

        return center

        # Red, Blue, Green, Yellow
MultiColorTrackerInstance = Tracker([
    [(136, 87, 111), (180, 255, 255)],
    [(99, 115, 150), (110, 255, 255)],
    [(56, 131, 155), (80, 255, 250)],
    [(22, 60, 200), (60, 255, 255)]
], 800)
for piFrame in MultiColorTrackerInstance.camera.capture_continuous(MultiColorTrackerInstance.rawCapture, format="bgr", use_video_port=True):
    frame = piFrame.array
    MultiColorTrackerInstance.capture(frame=frame)

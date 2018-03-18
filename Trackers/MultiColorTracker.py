"""
    Color detector
    >_ uses open cv to track a multiple colors as specified
"""

# import the necessary packages
from collections import deque
import numpy as np
import argparse
import sys
import imutils
import cv2
import colorsys
import matplotlib.pyplot as plt

class MultiColorTracker:
    '''
        iFollow robot class
    '''
    def __init__(self,colors):
        """
            Args: List of color tuples: [[(0,0,0),(255,255,255)]...]
        """
        self.colors = colors
        # capturing video through webcam
        self.camera = cv2.VideoCapture(0)
        self.status = "Running"
        self.minArea = 300

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

    def drawContours(self,masks,maskTuple,frame):
        color = maskTuple[1]
        mask = maskTuple[0]
        color_id = color
        contours=cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
        if len(contours) > 0:
            contour = max(contours, key=cv2.contourArea)
            area = cv2.contourArea(contour)
            if(area > self.minArea):
                print("Tracking Mask ",str(color))
                hh,s,v = color
                r,g,b = colorsys.hsv_to_rgb(hh,s,v)
                x,y,w,h = cv2.boundingRect(contour)
                frame = cv2.rectangle(frame,(x,y),(x+w,y+h),(self.cleanUpRGB(r,g,b)),2)
                cv2.putText(frame,str((self.cleanUpRGB(r,g,b)))+" color",(x,y),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (self.cleanUpRGB(r,g,b)))
    def cleanUpRGB(self,r,g,b):
        r = int(r) if int(r) > 0 else 0
        b = int(b) if int(b) > 0 else 0
        g = int(g) if int(g) > 0 else 0
        return r,g,b
    def createMasks(self,hsv,frame):
        masks = []
        for color in self.prepareColors():
            # finding the range of red,blue and yellow color in the image
            mask = cv2.inRange(hsv, color[0], color[1])
            mask = cv2.erode(mask, None, iterations=2)
            mask = cv2.dilate(mask, None, iterations=2)
            #Morphological transformation, Dilation
            kernal = np.ones((5 ,5), "uint8")
            mask = cv2.dilate(mask, kernal)
            #mask = cv2.bitwise_and(frame, frame, mask = mask)
            masks += [(mask,color[0])]
        return masks
    def capture(self, blur):
        # keep looping
        while True:
            # grab the current frame
            (grabbed, frame) = self.camera.read()
            # resize the frame, blur it, and convert it to the HSV
            # color space
            #frame = imutils.resize(frame, width=1080)
            blurred = cv2.GaussianBlur(frame, (11, 11), 0) if blur else frame
            hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
            ranges = []
            masks = self.createMasks(hsv,frame)
            # Track each color:
            for mask in masks:
                self.drawContours(masks,mask,frame)
            cv2.imshow("Color Tracking",frame)
            plt.imshow(frame, interpolation='none') # Plot the image, turn off interpolation
            plt.show() # Show the image window
            # cv2.imshow("red",res)
            if cv2.waitKey(10) & 0xFF == ord('q'):
                cap.release()
                cv2.destroyAllWindows()
                break


MultiColorTrackerInstance = MultiColorTracker([
                                                [(133,101,155),(154,140,255)],
                                                [(0,110,54),(30,147,255)],
                                                [(37,0,141),(56,107,245)]
                                                ])
MultiColorTrackerInstance.capture(True)

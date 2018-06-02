"""
    Color detector
    >_ uses open cv to track a certain color as specified
"""
# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
from collections import deque
import numpy as np
import argparse
import sys
import imutils
import cv2
from time import sleep

try:
    buffer = 64
    # define the lower and upper boundaries of the object's Color in HSV Space
    colorMin = (44, 70, 119)
    colorMax = (199, 255, 255)
    pts = deque(maxlen=buffer)
    # if a video path was not supplied, grab the reference
    # to the webcam
    # initialize the camera and grab a reference to the raw camera capture
    camera = PiCamera()
    rawCapture = PiRGBArray(camera)
    # keep looping
    for piFrame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        # grab the raw NumPy array representing the image, then initialize the timestamp
        # and occupied/unoccupied text
        frame = piFrame.array
        # resize the frame, blur it, and convert it to the HSV
        # color space
        frame = imutils.resize(frame, width=400)
        #blurred = cv2.GaussianBlur(frame, (11, 11), 0)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lower_range = np.array(colorMin, dtype=np.uint8)
        upper_range = np.array(colorMax, dtype=np.uint8)
        # construct a mask for the predefined color, then perform
        # a series of dilations and erosions to remove any small
        # blobs left in the mask
        mask = cv2.inRange(hsv, lower_range, upper_range)
        #mask = cv2.erode(mask, None, iterations=2)
        #mask = cv2.dilate(mask, None, iterations=2)
        # find contours in the mask and initialize the current
        # (x, y) center of the ball
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)[-2]
        center = None
        try:
            # only proceed if at least one contour was found
            if len(cnts) > 0:
                # find the largest contour in the mask, then use
                # it to compute the minimum enclosing circle and
                # centroid
                c = max(cnts, key=cv2.contourArea)
                ((x, y), radius) = cv2.minEnclosingCircle(c)
                M = cv2.moments(c)
                center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                # only proceed if the radius meets a minimum size
                if radius > 2:
                    # draw the circle and centroid on the frame,
                    # then update the list of tracked points
                    cv2.circle(frame, (int(x), int(y)), int(radius),
                               (255, 255, 255), 2)
                    cv2.circle(frame, center, 2, (0, 0, 255), -1)
        except:
            center = None

        # show the frame to our screen
        frame = cv2.flip(frame, 1)
        cv2.imshow("Color Tracking", frame)
        if cv2.waitKey(10) == 27:
            camera.release()
            cv2.destroyAllWindows()
            sys.exit()
            break  # esc to quit
        # clear the stream in preparation for the next frame
        rawCapture.truncate(0)

except KeyboardInterrupt:
    # cleanup the camera and close any open windows
    camera.release()
    cv2.destroyAllWindows()
    sys.exit()

"""
    Color detector
    >_ uses open cv to track a certain color as specified
"""
# import the necessary packages
import numpy as np
import sys
import imutils
import cv2
from time import sleep
while True:

    # define the lower and upper boundaries of the object's Color in HSV Space
    colorMin = (72, 72, 61)
    colorMax = (190, 255, 255)
    frame = cv2.imread("sample.jpg")
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    cv2.imshow("Color Tracking", hsv)
    lower_range = np.array(colorMin, dtype=np.uint8)
    upper_range = np.array(colorMax, dtype=np.uint8)
    mask = cv2.inRange(hsv, lower_range, upper_range)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    # find contours in the mask and initialize the current
    # (x, y) center of the ball
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)[-2]
    center = None
    for c in cnts:
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        if radius > 50 and radius < 200:
            cv2.circle(frame, (int(x), int(y)), int(radius),
                       (255, 255, 255), 2)
            cv2.circle(frame, center, 2, (0, 255, 0), -1)
            print(center)
    frame = cv2.flip(frame, 1)
    cv2.imshow("Color Tracking", frame)
    cv2.imwrite("output.png", frame)
    exit()
    if cv2.waitKey(10) == 27:
        break
        sys.exit()

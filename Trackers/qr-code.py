from __future__ import print_function
import pyzbar.pyzbar as pyzbar
import numpy as np
import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera
import math
import imutils


def decode(im):
    # Find barcodes and QR codes
    decodedObjects = pyzbar.decode(im)
    return decodedObjects


def distance(a, b):
    dist = math.hypot(b[0] - a[0], b[1] - a[1])
    return dist

# Display barcode and QR code location


def display(im, decodedObjects):

    # Loop over all decoded objects
    for decodedObject in decodedObjects:
        print(decodedObject.data.decode('utf-8'))
        if decodedObject.data.decode('utf-8') == "iFollow":
            points = decodedObject.polygon
            # If the points do not form a quad, find convex hull
            if len(points) > 4:
                hull = cv2.convexHull(
                    np.array([point for point in points], dtype=np.float32))
                hull = list(map(tuple, np.squeeze(hull)))
            else:
                hull = points

            # Number of points in the convex hull
            n = len(hull)

            # Draw the convext hull
            for j in range(0, n):
                cv2.line(im, hull[j], hull[(j+1) % n], (255, 0, 0), 3)
            print(points)
            center = distance(points[1], points[0]) / 2 + \
                points[3][0], distance(points[3], points[2])/2 + points[3][1]
            print(center)
            x, y = center

            cv2.circle(img, (int(x), int(y)), 2, (0, 255, 0), 10)


camera = PiCamera()
rawCapture = PiRGBArray(camera)
# keep looping
# Converts image to grayscale.
for piFrame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    frame = piFrame.array
    img = imutils.resize(frame, width=600)
    decodedObjects = decode(img)
    display(img, decodedObjects)
    cv2.imshow("#Qr Code tracker", img)

    # clear stream for next frame
    rawCapture.truncate(0)
    # Wait for the magic key
    keypress = cv2.waitKey(1) & 0xFF

    if keypress == ord('q'):
        break

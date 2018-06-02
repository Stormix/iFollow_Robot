"""
      _ _____     _ _                 ____       _           _
     (_)  ___|__ | | | _____      __ |  _ \ ___ | |__   ___ | |_
     | | |_ / _ \| | |/ _ \ \ /\ / / | |_) / _ \| '_ \ / _ \| __|
     | |  _| (_) | | | (_) \ V  V /  |  _ < (_) | |_) | (_) | |_
     |_|_|  \___/|_|_|\___/ \_/\_/   |_| \_\___/|_.__/ \___/ \__|

    iFollow - TIPE PROJECT
    @Authors : Anas Mazouni & Ismail Ouadrhiri
    @Date:   2017-06-07
    @Project: iFollow
    @Last modified time: 2018-03-30
"""

from UltrasonicSensor import distanceSensor
import math
from servoMotor import servoMotor
import IOSetup as IO
from motor import DCMotor as Motor
from time import sleep

# import colorTracker
from picamera.array import PiRGBArray
from picamera import PiCamera
from collections import deque
import numpy as np
import argparse
import sys
import imutils
import cv2

from PID import PID


class iFollow:
    '''
        iFollow robot class
    '''

    def __init__(self):

        self.UltrasonicSensors = {
            "ObstacleSensor": distanceSensor("Obstacle", IO.TRIG1, IO.ECHO1),
            "DistanceSensor": distanceSensor("Distance", IO.TRIG2, IO.ECHO2)
        }
        self.Motors = {
            "LEFT": Motor("LEFT", IO.MOTOR_L_X, IO.MOTOR_L_X),
            "RIGHT": Motor("RIGHT", IO.MOTOR_R_X, IO.MOTOR_R_X)
        }
        self.servoMotor = servoMotor(0, IO.SERVO)
        self.status = "Running"
        # Camera resolution
        self.cameraHeight = 400
        self.cameraWidth = 400
        # Servo Angle Steps
        self.Step = 10
        # Vitesse Consigne
        self.setSpeed = 50
        # Obstacle detection distance limit, an Obstacle will be considered
        # detected if the separating distance is less than it.
        self.detectionDistance = 3
        self.setTrackingEps = 10  # Erreur accepte

    def __str__(self):
        '''
            Object Representation
        '''
        distance = 10  # self.UltrasonicSensors["DistanceSensor"].mesureDistance()
        obstacle = self.UltrasonicSensors["ObstacleSensor"].isObstacleDetected(
        )
        motorL = self.Motors["LEFT"].status
        motorR = self.Motors["RIGHT"].status
        servoAngle = self.servoMotor.lastAngle
        # Running, Following, Disabled
        return """
                      _ _____     _ _                 ____       _           _
                     (_)  ___|__ | | | _____      __ |  _ \ ___ | |__   ___ | |_
                     | | |_ / _ \| | |/ _ \ \ /\ / / | |_) / _ \| '_ \ / _ \| __|
                     | |  _| (_) | | | (_) \ V  V /  |  _ < (_) | |_) | (_) | |_
                     |_|_|  \___/|_|_|\___/ \_/\_/   |_| \_\___/|_.__/ \___/ \__|

                        > Status : {}
                        > Sensors :
                                Distance Sensor : {} cm
                                Obstacle Sensor : {}
                        > Servo Angle : {} degree
                        > Camera :
                                Object (not) detected
                        > Motors :
                            Motor Left: {}
                            Motor Right: {}
                """.format(self.status, distance, obstacle,  servoAngle,  motorL,  motorR)

    def trackPerson(self, tracker="color"):

        pid = PID(10.2, 0.01, 0.001)
        pid.SetPoint = 0.0
        pid.setSampleTime(0.0)
        # Color tracker
        if tracker == "color":
            try:
                # define the lower and upper boundaries of the object's Color in HSV Space
                colorMin = (44, 70, 119)
                colorMax = (199, 255, 255)
                # initialize the camera and grab a reference to the raw camera capture
                camera = PiCamera()
                rawCapture = PiRGBArray(camera)
                # keep looping
                for piFrame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
                    # clear the stream in preparation for the next frame
                    rawCapture.truncate(0)
                    # grab the raw NumPy array representing the image, then initialize the timestamp
                    # and occupied/unoccupied text
                    frame = piFrame.array
                    # resize the frame, blur it, and convert it to the HSV
                    # color space
                    frame = imutils.resize(frame, width=self.cameraWidth)
                    frame = cv2.flip(frame, 1)
                    # blurred = cv2.GaussianBlur(frame, (11, 11), 0)
                    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                    lower_range = np.array(colorMin, dtype=np.uint8)
                    upper_range = np.array(colorMax, dtype=np.uint8)
                    # construct a mask for the predefined color, then perform
                    # a series of dilations and erosions to remove any small
                    # blobs left in the mask
                    mask = cv2.inRange(hsv, lower_range, upper_range)
                    # mask = cv2.erode(mask, None, iterations=2)
                    # mask = cv2.dilate(mask, None, iterations=2)
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
                            center = (int(M["m10"] / M["m00"]),
                                      int(M["m01"] / M["m00"]))
                            # only proceed if the radius meets a minimum size
                            x = center[0]-self.cameraWidth/2
                            self.followDirection(x, pid)
                    except:
                        pass
                    # clear the stream in preparation for the next frame
                    rawCapture.truncate(0)
            except KeyboardInterrupt:
                # cleanup the camera and close any open windows
                camera.release()
                cv2.destroyAllWindows()

    def detectObstacle(self):
        """
            We're using a the seconds sensor to detect obstacles
        """
        return self.UltrasonicSensors["ObstacleSensor"].isObstacleDetected()

    def followDirection(self, x, pid):  # Get tracked object center coordinates
        servoMaxAngle = self.servoMotor.maxAngle
        Step = self.Step
        # Currently outside the tracking premise
        servoCurrentAngle = self.servoMotor.lastAngle
        # self.UltrasonicSensors["DistanceSensor"].mesureDistance()
        # distance = 10
        # print(x/distance)
        # angle = math.atan(x/distance)
        # Rotate the servo motor to the calculated angle
        # pid.update(x)
        # output = pid.output
        # print(x, output)
        # setAngle = output
        Kp = 1
        setAngle = servoCurrentAngle
        if x > 0:
            setAngle += Step * Kp
        elif x < 0:
            setAngle -= Step * Kp
        print(x, servoCurrentAngle, setAngle)
        if setAngle != servoCurrentAngle:
            self.servoMotor.setServoAngle(int(setAngle))

    def followPerson(self):
        x, y = self.trackPerson()
        pass

    def shutdown(self):
        # Stop everyting & cleanup
        GPIO.cleanup()

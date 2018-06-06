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
from Trackers import SingleColorTracker
from Trackers import QRCode

# import colorTracker
from collections import deque
import numpy as np
import argparse
import sys
import imutils
import cv2
import subprocess
from multiprocessing import Process

from PID import PID


class iFollow:
    '''
        iFollow robot class
    '''

    def __init__(self):

        self.servoMotor = servoMotor(0, IO.SERVO)
        self.status = "Running"
        self.password = "iFollow"
        # Camera resolution
        self.cameraWidth = 400
        # Servo Angle Steps
        self.Step = 10
        # Vitesse Consigne
        self.setSpeed = 50
        # Obstacle detection distance limit, an Obstacle will be considered
        # detected if the separating distance is less than it.
        self.detectionDistance = 3
        self.TrackerSetPoint = 10
        self.cameraPixelCm = 22
        self.UltrasonicSensors = {
            "DistanceSensor": distanceSensor("Distance", IO.TRIG1, IO.ECHO1),
            "ObstacleSensor": distanceSensor("Obstacle", IO.TRIG2, IO.ECHO2, self.detectionDistance)
        }
        self.Motors = {
            "LEFT": Motor("LEFT", IO.MOTOR_L_X, IO.MOTOR_L_X),
            "RIGHT": Motor("RIGHT", IO.MOTOR_R_X, IO.MOTOR_R_X)
        }

    def __str__(self):
        '''
            Object Representation
        '''
        distance = 10  # self.UltrasonicSensors["DistanceSensor"].mesureDistance()
        obstacle = self.detectObstacle()
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
        pid = PID(1, 0.4, 0.001)
        # Color tracker
        if tracker == "color":
            # define the lower and upper boundaries of the object's Color in HSV Space
            colorMin = (82, 93, 0)
            colorMax = (255, 255, 209)
            Tracker = SingleColorTracker.Tracker(
                [colorMin, colorMax], self.cameraWidth)
            for piFrame in Tracker.camera.capture_continuous(Tracker.rawCapture, format="bgr", use_video_port=True):
                frame = piFrame.array
                # try:
                x = Tracker.getCoordinate(False, frame)
                if x:
                    x -= self.cameraWidth / 2
                else:
                    x = 0
                # except:
                #    print(sys.exc_info())
                #    x = 0
                self.followDirection(x, pid)
                Tracker.rawCapture.truncate(0)
        elif tracker == "QRCode":
            Tracker = QRCode.Tracker(self.password, 400)
            for piFrame in Tracker.camera.capture_continuous(Tracker.rawCapture, format="bgr", use_video_port=True):
                frame = piFrame.array
                x, y = Tracker.getCenter(frame)
                if x:
                    x -= self.cameraWidth / 2
                else:
                    x = 0
                print(x)
                self.followDirection(-x, pid)
                Tracker.rawCapture.truncate(0)
        else:
            pass

    def detectObstacle(self):
        """
            We're using a the seconds sensor to detect obstacles
        """
        return self.UltrasonicSensors["ObstacleSensor"].isObstacleDetected()

    # Get tracked object center coordinates
    def followDirection(self, x, pid, method="angle"):
        servoMaxAngle = self.servoMotor.maxAngle
        servoStep = self.Step
        # Currently outside the tracking premise
        servoCurrentAngle = self.servoMotor.lastAngle
        """if statemnts"""
        if method == "if":
            Kp = 1
            setAngle = servoCurrentAngle
            if x > 0:
                setAngle += servoStep * Kp
            elif x < 0:
                setAngle -= servoStep * Kp
            print(x, servoCurrentAngle, setAngle)
            if setAngle != servoCurrentAngle:
                self.servoMotor.setServoAngle(int(setAngle))
        elif method == "angle":
            # 22 pixel per centimeter
            distance = 16 * self.cameraPixelCm  # self.mesureDistance() * 22
            objectAngle = math.atan(float(x)/float(distance))
            objectAngle = round(math.degrees(objectAngle), 2)
            # set point is 10 so
            # setAngle = - math.degrees(1.627)
            setAngle = objectAngle + servoCurrentAngle
            if setAngle > 90:
                while setAngle > 90:
                    setAngle -= 1
            print("Distance: "+str(objectAngle), "Current:"+str(servoCurrentAngle),
                  "Setpoint: "+str(setAngle), x)
            self.servoMotor.setServoAngle(setAngle)
            return setAngle
        else:
            # PID
            distance = 16 * 22  # 20pixel per centimeter
            pid.SetPoint = 0
            pid.setSampleTime(0.0)
            pid.update(x)
            x = -pid.output
            setAngle = math.atan(float(x)/float(distance))
            setAngle = math.degrees(setAngle)
            if setAngle > 90:
                while setAngle > 90:
                    setAngle -= 1
            print(servoCurrentAngle, setAngle, x)
            self.servoMotor.setServoAngle(setAngle)

    def followPerson(self):
        self.status = "Running"
        self.runInParallel(self.trackPerson, self.keepDistance)

    def mesureDistance(self):
        #
        output = subprocess.Popen(["python", "ultrasonTest.py"],
                                  stdout=subprocess.PIPE).communicate()[0]
        return float(output)

    def keepDistance(self):
        pass

    def shutdown(self):
        # Stop everyting & cleanup
        GPIO.cleanup()

    @staticmethod
    def runInParallel(*fns):
        proc = []
        for fn in fns:
            p = Process(target=fn)
            p.start()
            proc.append(p)
        for p in proc:
            p.join()

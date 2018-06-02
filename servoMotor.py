"""
    Servo Motor module
    >_ Controls the servo motor
"""

import RPi.GPIO as GPIO
from time import sleep
import ServoBlaster


class servoMotor:
    '''
        servoMotor class
    '''

    def __init__(self, ID, SERVO_PIN):

        # ServoBlaster is what we use to control the servo motors

        self.SERVO_PIN = 11 if SERVO_PIN == 17 else 0  # Pin 17 is physical 11
        self.ID = ID
        self.lastAngle = 0
        self.minAngle = -90
        self.maxAngle = 90
        self.HIGH_LIM = 2000
        self.LOW_LIM = 1000

    def __str__(self):
        return """ Servo Motor #{} at {} degrees """.format(self.ID, self.lastAngle)

    def reset(self):
        # Initialize the servo motor
        print("Positioning servo to initial position.")
        self.setServoAngle(0)

    def customMap(self, x, in_min, in_max, out_min, out_max):
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

    def setServoAngle(self, position):
        """
            Sets the servo angle
            params:
                position : int : (-90,90)
        """
        if position <= self.maxAngle and position >= self.minAngle:
            # 1000us/2000us is normally the extremes and 1500us is centered.
            pulse = int(self.customMap(position, self.minAngle,
                                       self.maxAngle, self.LOW_LIM, self.HIGH_LIM))
            self.lastAngle = position
            ServoBlaster.servo_set(self.SERVO_PIN, str(pulse)+"us")
            print("Set servo to : ", position, pulse)

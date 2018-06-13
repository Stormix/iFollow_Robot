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
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(SERVO_PIN, GPIO.OUT)
        self.SERVO_PIN = SERVO_PIN
        self.ID = ID
        self.lastAngle = 0
        self.minAngle = 0
        self.maxAngle = 180

    def __str__(self):
        return """ Servo Motor #{} at {} degrees """.format(self.ID, self.lastAngle)

    def reset(self):
        # Initialize the servo motor
        print("Positioning servo to initial position.")
        self.setServoAngle(0)

    def customMap(self, x, in_min, in_max, out_min, out_max):
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

    def setServoAngle(self, angle):
        """
            Sets the servo angle
            params:
                position : int : (-90,90)
        """
        if angle <= self.maxAngle and angle >= self.minAngle:
            servo = self.SERVO_PIN
            pwm = GPIO.PWM(servo, 50)
            pwm.start(8)
            dutyCycle = angle / 18. + 3.
            pwm.ChangeDutyCycle(dutyCycle)
            sleep(0.3)
            pwm.stop()

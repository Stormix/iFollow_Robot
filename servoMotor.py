"""
    Servo Motor module
    >_ Controls the servo motor
"""

import RPi.GPIO as GPIO
from time import sleep


class servoMotor:
    '''
        servoMotor class
    '''

    def __init__(self, ID, SERVO_PIN):

        GPIO.setup(SERVO_PIN, GPIO.OUT)
        self.SERVO_PIN = SERVO_PIN
        self.ID = ID
        self.lastAngle = 0
        self.maxAngle = 180

    def __str__(self):
        return """ Servo Motor #{} at {} degrees """.format(self.ID, self.lastAngle)

    def reset(self):
        # Initialize the servo motor
        print("Positioning servo to initial position.")
        self.setServoAngle(0)

    def setServoAngle(self, angle):
        """
            Sets the servo angle
        """
        angle = angle if angle < 180 else angle - 180
        self.lastAngle = angle
        servo = self.SERVO_PIN
        pwm = GPIO.PWM(servo, 50)
        pwm.start(8)
        dutyCycle = angle / 18. + 3.
        pwm.ChangeDutyCycle(dutyCycle)
        sleep(0.3)
        pwm.stop()

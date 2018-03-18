"""
    Motor module
    >_ Controls the motor
"""

import RPi.GPIO as GPIO

class DCMotor:
    '''
        DC-Motor class
    '''

    def __init__(self, ID, MOTOR_X, MOTOR_Y):

        GPIO.setup(MOTOR_X, GPIO.OUT)
        GPIO.setup(MOTOR_Y, GPIO.OUT)

        self.motorPWM_Forward = GPIO.PWM(MOTOR_X, 50)
        self.motorPWM_Backward = GPIO.PWM(MOTOR_Y, 50)

        self.motorPWM_Forward.start(0)
        self.motorPWM_Backward.start(0)

        self.status = "Stopped"

    def __str__(self):
        return """ Motor #{} : {}""".format(self.ID, self.status)

    def mesureSpeed(self):
        pass

    def moveForward(self, speed = 50):

        self.status = "Forward"
        self.motorPWM_Forward.ChangeDutyCycle(speed)

    def moveBackward(self, speed = 50):

        self.status = "Backward"
        self.motorPWM_Backward.ChangeDutyCycle(speed)

    def stop(self):

        self.status = "Stopped"
        self.motorPWM_Forward.ChangeDutyCycle(0)
        self.motorPWM_Backward.ChangeDutyCycle(0)

"""
    Motor module
    >_ Controls the motor
"""

import RPi.GPIO as GPIO


class DCMotor:
    '''
        DC-Motor class
    '''

    def __init__(self, ID, MOTOR_X, MOTOR_Y, ENABLE):

        GPIO.setup(MOTOR_X, GPIO.OUT)
        GPIO.setup(MOTOR_Y, GPIO.OUT)
        GPIO.setup(ENABLE, GPIO.OUT)
        self.MOTOR_X = MOTOR_X
        self.MOTOR_Y = MOTOR_Y
        self.motorPWM = GPIO.PWM(ENABLE, 50)

        self.motorPWM.start(0)

        self.status = "Stopped"

    def __str__(self):
        return """ Motor #{} : {}""".format(self.ID, self.status)

    def mesureSpeed(self):
        pass

    def moveForward(self, speed=50):

        self.status = "Forward"

        GPIO.output(self.MOTOR_X, True)
        GPIO.output(self.MOTOR_Y, False)

        self.motorPWM.ChangeDutyCycle(speed)

    def moveBackward(self, speed=50):

        self.status = "Backward"
        GPIO.output(self.MOTOR_X, False)
        GPIO.output(self.MOTOR_Y, True)

        self.motorPWM.ChangeDutyCycle(speed)

    def move(self, speed=50):
        if speed > 0:
            self.status = "Forward"
            GPIO.output(self.MOTOR_X, True)
            GPIO.output(self.MOTOR_Y, False)
        else:
            self.status = "Backward"
            GPIO.output(self.MOTOR_X, False)
            GPIO.output(self.MOTOR_Y, True)
        print(self.status)
        self.motorPWM.ChangeDutyCycle(abs(speed))

    def stop(self):

        self.status = "Stopped"
        self.motorPWM.ChangeDutyCycle(0)

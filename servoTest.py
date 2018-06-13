import RPi.GPIO as GPIO
import time
from servoMotor import servoMotor


servo = servoMotor(0, 17)
for i in range(20, 100, 10):
    servo.setServoAngle(i)
    time.sleep(2)

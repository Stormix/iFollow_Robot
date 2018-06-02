from servoMotor import servoMotor
import RPi.GPIO as GPIO
from UltrasonicSensor import distanceSensor
import IOSetup as IO
from time import sleep
# Setup the raspberry pi GPIO

Servo = servoMotor(0, 17)
print(Servo)

# val = 0
# direction = 1
while True:
    angle = int(input("Angle: "))
    Servo.setServoAngle(angle)

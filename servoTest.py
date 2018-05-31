from servoMotor import servoMotor
import RPi.GPIO as GPIO

# Setup the raspberry pi GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
Servo = servoMotor(0, 02)
print(Servo)
while True:
    angle = int(input("Angle : "))
    Servo.setServoAngle(angle+30)
    print(Servo)

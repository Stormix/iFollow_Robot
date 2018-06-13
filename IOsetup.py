"""
    I/O setup module
    >_ sets up each input & output of the raspberry pi
"""
#
import RPi.GPIO as GPIO

# Setup the raspberry pi GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Setup ultrasonic sensor

ECHO = 2
TRIG = 3
SERVO = 4

# LEFT MOTOR
MOTOR_L_X = 25
MOTOR_L_Y = 24
MOTOR_L_ENABLE = 23

# RIGHT MOTOR
MOTOR_R_X = 22
MOTOR_R_Y = 27
MOTOR_R_ENABLE = 10


ENCODER = 26
TEMP_SENSOR = 13

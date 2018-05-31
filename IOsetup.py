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

TRIG1 = 03
ECHO1 = 04

TRIG2 = 18
ECHO2 = 17

SERVO = 02

# LEFT MOTOR
MOTOR_L_X = 10
MOTOR_L_Y = 12

# RIGHT MOTOR
MOTOR_R_X = 11
MOTOR_R_Y = 12

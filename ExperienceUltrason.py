"""
    Experiences ultrason
"""

import distanceSensor.UltrasonicSensor as UltrasonicSensor
import IOSetup as IO
UltrasonicSensor(0, IO.TRIG1, IO.ECHO1)

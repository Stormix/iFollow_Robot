"""
    Experiences ultrason
"""

from UltrasonicSensor import distanceSensor
import IOSetup as IO
from time import sleep


while True:
    Sensor1 = distanceSensor(0, IO.TRIG1, IO.ECHO1)
    mesure = Sensor1.mesureDistance()
    tmp = mesure[1]
    dist = mesure[0]
    print(str(dist)+"cm")
    if int(dist) > 500:
        quit()
    sleep(2)

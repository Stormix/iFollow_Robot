from UltrasonicSensor import distanceSensor

import IOSetup as IO

Sensor = distanceSensor(1, IO.TRIG1, IO.ECHO1)
print(Sensor.mesureDistance())

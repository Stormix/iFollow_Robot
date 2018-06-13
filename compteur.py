###########
import time
import pigpio
from motor import DCMotor
import math
import IOSetup as IO
from PID import PID
from random import randint
WIND_GPIO = 4
pi = pigpio.pi()  # connect to Pi

if not pi.connected:
    exit()

pi.set_mode(WIND_GPIO, pigpio.INPUT)
pi.set_pull_up_down(WIND_GPIO, pigpio.PUD_UP)
wind_cb = pi.callback(WIND_GPIO, pigpio.FALLING_EDGE)
motor = DCMotor(0, IO.MOTOR_L_X, IO.MOTOR_L_Y, IO.MOTOR_L_ENABLE)
# motor.moveForward(10)

pid = PID(1, 0.1, 0)
pid.setSampleTime = 0.0
for i in range(10):
    erreur_acc = 1
    setpoint = randint(-5, 5) * 30.3
    print(setpoint)
    pid.SetPoint = abs(setpoint)
    try:
        while True:
            # time.sleep(0.01)
            count = wind_cb.tally()
            #number = count - old_count
            nbdetours = count/20
            rad = nbdetours * 2*math.pi
            pid.update(rad)
            output = pid.output
            print("PID : {}, Counter: {}".format(pid.output, rad), setpoint)
            if output < erreur_acc:
                break
            if setpoint > 0:
                motor.moveForward(output)
            else:
                motor.moveBackward(output)

    except KeyboardInterrupt:
        motor.stop()
        pi.stop()

    time.sleep(5)

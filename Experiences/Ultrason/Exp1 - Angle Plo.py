import numpy as np
import matplotlib.pyplot as plt
# from UltrasonicSensor import distanceSensor
# import IOSetup as IO
from time import sleep
from math import pi
import random
angleMesure = range(-90, 90, 10)
angleMesureRad = [float(i) * pi / 180.0 for i in angleMesure]
# Sensor1 = distanceSensor(0, IO.TRIG1, IO.ECHO1)
ax = plt.subplot(polar=True)
ax.set_thetamin(-91)
ax.set_thetamax(91)
ax.set_theta_direction(-1)
ax.set_rmax(100)
# ax.set_rmin(70.0)
ax.grid(True)
ax.set_theta_zero_location("N")
ax.set_title("Angle de mesure Ultrason")
distances = {}
# for i in range(2, 22, 2):
#     distances[i] = []
#     for angle in angleMesure:
#         print("Positionner a {} deg et {}cm".format(angle, i))
#         sleep(5)
#         mesure = Sensor1.mesureDistance()
#         tmp = mesure[1]
#         dist = mesure[0] if mesure[0] < 22 else 0
#         distances[i] += [dist]
# print(distances)
distances = {2: [0, 0, 0, 0, 0, 6.4, 5.58, 5.12, 4.69, 4.22, 4.52, 5.37, 6, 5.34, 0, 0, 0, 0],
             4: [0, 0, 0, 0, 0, 0, 0, 0, 0, 5.46, 5.91, 0, 0, 0, 0, 0, 0, 0],
             6: [0, 0, 0, 0, 0, 0, 0, 0, 8.09, 6.87, 8.77, 0, 0, 0, 0, 0, 0, 0],
             8: [0, 0, 0, 0, 0, 0, 0, 9.66, 8.77, 8.25, 8.77, 12.12, 0, 0, 0, 0, 0, 0],
             10: [0, 0, 0, 0, 0, 0, 0, 0, 11.09, 10.3, 10.35, 10.54, 0, 0, 0, 0, 0, 0],
             12: [0, 0, 0, 0, 0, 0, 0, 13.06, 13.04, 13.56, 12.99, 12.97, 0, 0, 0, 0, 0, 0],
             14: [0, 0, 0, 0, 0, 0, 0, 14.05, 14.64, 14.5, 14.42, 15.23, 0, 0, 0, 0, 0, 0],
             16: [0, 0, 0, 0, 0, 0, 0, 0, 17.39, 16.98, 17.34, 0, 0, 0, 0, 0, 0, 0],
             18: [0, 0, 0, 0, 0, 0, 0, 0, 21.45, 21.27, 21.81, 0,  0, 0, 0, 0, 0, 0]}

colors = ['b', 'g', 'r', 'm', 'y', 'c']
for dist in distances.keys():
    distance = distances[dist]
    color = random.choice(colors)
    ax.plot(angleMesureRad, distance, color=color,
            linewidth=1, label=str(dist)+"cm")

    ax.fill_between(angleMesureRad, distance,
                    color=color, alpha=0.5)
plt.legend()
plt.savefig("Experiences/Ultrason/graphes/Angle.png")

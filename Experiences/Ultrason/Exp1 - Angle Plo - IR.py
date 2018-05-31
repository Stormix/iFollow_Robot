import numpy as np
import matplotlib.pyplot as plt
# from UltrasonicSensor import distanceSensor
# import IOSetup as IO
from time import sleep
from math import pi
import random
import serial

angleMesure = range(-90, 90, 10)
angleMesureRad = [float(i) * pi / 180.0 for i in angleMesure]
# # Sensor1 = distanceSensor(0, IO.TRIG1, IO.ECHO1)
ax = plt.subplot(polar=True)
ax.set_thetamin(-91)
ax.set_thetamax(91)
ax.set_theta_direction(-1)
# ax.set_rmax(700)
# ax.set_rmin(70.0)
ax.grid(True)
ax.set_theta_zero_location("N")
ax.set_title("Cone de detection")
# ser = serial.Serial('COM5', 9600, timeout=0)
# distances = {}

# for dist in range(3, 22, 2):
#     distances[dist] = []
#     for angle in angleMesure:
#         print("Positionner a {} deg et {}cm".format(angle, dist))
#         sleep(2)
#         print("mesuring .. ", end="")
#         average = 9999
#         while average == 9999:
#             msg = ser.readline().decode("utf-8", errors="ignore")
#             if msg != '':
#                 try:
#                     valeurs = []
#                     for i in range(10):
#                         valeurs += [float(msg)]
#                     average = np.average(valeurs) if np.average(
#                         valeurs) > 85 else 0
#                 except ValueError:
#                     continue
#         print(average)
#         distances[dist] += [average]
# print(distances)

# distances = {2: [0, 0, 0, 0, 0, 8.4, 7.58, 5.12, 4.69, 4.22, 4.52, 5.37, 7.99, 5.34, 6.92, 8.92, 7.57, 0],
#              4: [0, 0, 0, 0, 0, 0, 0, 0, 0, 5.46, 5.91, 0, 0, 0, 0, 0, 0, 0], 6: [0, 0, 0, 0, 0, 0, 0, 0, 8.09, 6.87, 8.77, 0, 0, 0, 0, 0, 0, 0], 8: [0, 0, 0, 0, 0, 0, 11.2, 9.66, 8.77, 8.25, 8.77, 12.12, 0, 0, 0, 0, 0, 0], 10: [0, 0, 0, 0, 0, 0, 0, 0, 11.09, 10.3, 10.35, 10.54, 0, 0, 0,
#                                                                                                                                                                                                                                      0, 0, 0], 12: [0, 0, 0, 0, 0, 0, 0, 13.06, 13.04, 12.56, 12.99, 12.97, 14.98, 0, 0, 0, 0, 0], 14: [0, 0, 0, 0, 0, 0, 0, 17.05, 14.64, 14.5, 14.42, 15.23, 0, 0, 0, 0, 0, 0], 16: [0, 0, 0, 0, 0, 0, 0, 17.87, 17.39, 16.98, 17.34, 17.27, 0, 0, 0, 0, 0, 0], 18: [0, 0, 0, 0, 0, 0, 0, 0, 21.45, 21.27, 21.81, 0,  0, 0, 0, 0, 0, 0], 20: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]}
#
distances = {
    3: [0, 0, 0, 0, 0, 0, 0, 549.0, 590.0, 615.0, 602.0, 603.0, 467.0, 0, 0, 0, 0, 0],
    5: [0, 0, 0, 0, 0, 0, 0, 0, 407.0, 436.0, 451.0, 554.0, 0, 0, 0, 0, 0, 0],
    7: [0, 0, 0, 0, 0, 0, 0, 0, 287.0, 322.0, 493.0, 441.0, 0, 0, 0, 0, 0, 0],
    9: [0, 0, 0, 0, 0, 0, 0, 0, 120.0, 252.0, 389.0, 412.0, 0, 0, 0, 0, 0, 0],
    11: [0, 0, 0, 0, 0, 0, 0, 0, 140.0, 211.0, 348.0, 357.0, 0, 0, 0, 0, 0, 0],
    13: [0, 0, 0, 0, 0, 0, 0, 0, 180.0, 334.0, 246.0, 0, 0,  0, 0, 0, 0, 0],
    15: [0, 0, 0, 0, 0, 0, 0, 0, 164.0, 299.0, 195.0, 0,  0, 0, 0, 0, 0, 0],
    17: [0, 0, 0, 0, 0, 0, 0, 0, 150.0, 281.0, 168.0, 0,  0, 0, 0, 0, 0, 0],
    19: [0, 0, 0, 0, 0, 0, 0, 0, 120.0, 203.0, 179.0, 0,  0, 0, 0, 0, 0, 0],
    21: [0, 0, 0, 0, 0, 0, 0, 0, 105.0, 101.0, 116.0, 0, 0, 0, 0, 0, 0, 0]}

colors = ['b', 'g', 'r', 'm', 'y', 'c']
for dist in distances.keys():
    distance = distances[dist]
    Y = []
    for d in distance:
        Y += [d if d == 0 else 700-d]
    color = random.choice(colors)
    ax.plot(angleMesureRad, distance, color=color,
            linewidth=1, label=str(dist)+"cm")

    ax.fill_between(angleMesureRad, distance,
                    color=color, alpha=0.5)
plt.legend()
plt.title('Cone de mesure IR')
plt.show()
plt.savefig("Experiences/Ultrason/graphes/Angle-IR.png")

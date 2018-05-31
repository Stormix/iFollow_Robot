"""
    Experiences ultrason
"""

from UltrasonicSensor import distanceSensor
import IOSetup as IO
from time import sleep


# print("Experience 1: --------------")

# X = [i for i in range(0, 280, 10)]
# Y = []
# T = []

# print("Prochaine mesure a 0cm")
# sleep(4)
# for i in range(len(X)):
#     Sensor1 = distanceSensor(0, IO.TRIG1, IO.ECHO1)
#     mesure = Sensor1.mesureDistance()
#     tmp = mesure[1]
#     dist = mesure[0]
#     Y += [dist]
#     T += [tmp]
#     print("Mesure prochaine a "+str(X[i] + 10) + "cm")
#     sleep(4)

# print(X, Y, T)
X = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140,
     150, 160, 170, 180, 190, 200, 210, 220, 230, 240, 250, 260, 270]
Y = [2937.69, 10.25, 21.61, 31.89, 42.6, 49.94, 59.7, 69.21, 78.98, 88.72, 99.16, 110.4, 108.53, 127.81,
     136.65, 147.15, 142.2, 166.82, 176.87, 187.36, 197.12, 208.81, 216.34, 227.1, 2954.6, 245.02, 257.14, 141.43]
T = [0.0864025354385376, 0.0003014802932739258, 0.0006355047225952148, 0.0009380578994750977, 0.0012530088424682617, 0.0014688968658447266, 0.0017559528350830078, 0.00203549861907959, 0.0023230314254760742, 0.0026094913482666016, 0.0029164552688598633, 0.0032470226287841797, 0.0031920671463012695, 0.003759026527404785,
     0.004019021987915039, 0.004328012466430664, 0.00418245792388916, 0.0049065351486206055, 0.005202054977416992, 0.005510449409484863, 0.0057975053787231445, 0.0061414241790771484, 0.006363034248352051, 0.006679534912109375, 0.08689999580383301, 0.007206439971923828, 0.007562994956970215, 0.00415956974029541]
# Vitesse du son a la temperature mesuree: (344.854, 22.0)

#print("Vitesse du son a la temperature mesuree: "+str(Sensor1.getSoundSpeed()))
log = open("Experiences/Ultrason/Exp1.txt", "a")
log.write("X = "+str(X)+"\n")
log.write("Y = " + str(Y)+"\n")
log.write("T = " + str(T)+"\n")
log.write("Vitesse du son a la temperature mesuree: (344.854, 22.0)")
log.close()

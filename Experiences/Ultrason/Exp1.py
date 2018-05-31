"""
 Distance mesuree vs Distance reel
"""

import matplotlib.pyplot as plt
import numpy as np
from slugify import slugify
import random

colors = ['b', 'g', 'r', 'm', 'y', 'c']
X = [i+2 for i in range(0, 90, 2)]
Y = [4.52, 4.98, 6.94, 8.67, 10.85, 10.57, 15.28, 16.69, 19.21, 23.93, 23.73, 25.13, 26.65, 28.22, 30.07, 31.94, 33.98, 36.02, 38.06, 39.87, 41.45, 43.32,
     45.22, 47.17, 49.32, 51.1, 53.4, 55.03, 57.22, 59.24, 59.24, 62.71, 65.13, 66.52, 68.59, 70.8, 72.86, 74.46, 76.45, 78.68, 80.83, 82.69, 85.44, 87.11, 87.72]

Dreel = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140,
         150, 160, 170, 180, 190, 200, 210, 220, 230, 240, 250, 260, 270]
Dmes = [10.25, 21.61, 31.89, 42.6, 49.94, 59.7, 69.21, 78.98, 88.72, 99.16, 110.4, 108.53, 127.81,
        136.65, 147.15, 142.2, 166.82, 176.87, 187.36, 197.12, 208.81, 216.34, 227.1, 239.6, 245.02, 257.14, 271.43]
T = [0.0003014802932739258, 0.0006355047225952148, 0.0009380578994750977, 0.0012530088424682617, 0.0014688968658447266, 0.0017559528350830078, 0.00203549861907959, 0.0023230314254760742, 0.0026094913482666016, 0.0029164552688598633, 0.0032470226287841797, 0.0031920671463012695, 0.003759026527404785,
     0.004019021987915039, 0.004328012466430664, 0.00418245792388916, 0.0049065351486206055, 0.005202054977416992, 0.005510449409484863, 0.0057975053787231445, 0.0061414241790771484, 0.006363034248352051, 0.006679534912109375, 0.00689999580383301, 0.007206439971923828, 0.007562994956970215, 0.00785956974029541]

Velocity = 344.854
DmesTemp = [round(float(Time * Velocity * 100), 2) for Time in T]


# Vitesse du son a la temperature mesuree: (344.854, 22.0)


xlabel = 'Distance Réelle (cm)'  # ex : 'Axe des X'
ylabel = 'Distance Mesurée (cm)'  # ex : 'Axe des Y'
title = 'Linéarite des mesures du capteur Ultrason HC-SR04'  # ex : 'Titre du graphe'

plt.plot(np.array(X), np.array(Y),
         color="c", label=ylabel)
plt.plot(np.array(X), np.array(X), color="m", label=xlabel)
plt.xlabel(xlabel)
plt.ylabel(ylabel)
plt.title(title)
plt.grid(True)
plt.legend(loc='lower right')
plt.savefig("graphes/"+title+" - 1m.png")
print('Graphe 0 Cree ! ✔')


xlabel = 'Distance Réelle (cm)'  # ex : 'Axe des X'
ylabel = 'Distance Mesurée (cm)'  # ex : 'Axe des Y'
title = 'Linéarite des mesures du capteur Ultrason HC-SR04'  # ex : 'Titre du graphe'

plt.plot(np.array(Dreel), np.array(Dmes),
         color="c", label=ylabel)
plt.plot(np.array(Dreel), np.array(Dreel), color="m", label=xlabel)
plt.plot(np.array(Dreel), np.array(DmesTemp), color="g",
         label="Distance Mesurée (avec Temp.) (cm)")
plt.xlabel(xlabel)
plt.ylabel(ylabel)
plt.title(title)
plt.grid(True)
plt.legend(loc='lower right')
plt.savefig("graphes/"+title+" - 3m.png")
print('Graphe 1 Cree ! ✔')


Erreur = [abs(v - u) / v * 100 for u, v in zip(Dmes, Dreel)]

xlabel = 'Distance Réelle (cm)'  # ex : 'Axe des X'
ylabel = 'Erreur mesurée ' + r'$\epsilon$' + ' (%)'  # ex : 'Axe des Y'
title = 'Erreur en fonction de la distance mesure'  # ex : 'Titre du graphe'

plt.clf()
plt.plot(np.array(Dreel), np.array(Erreur),
         color="m", label=r'$\epsilon$' + ' (%)')
plt.plot(np.array(Dreel), [np.average(Erreur)] * len(Dreel),
         color="c", label=r'$\epsilon$' + ' moyen (%)')

plt.text(275, 2.6, r'$\epsilon$' + '= '+str(round(np.average(Erreur), 2))+'%')
Erreur = [abs(v - u) / v * 100 for u, v in zip(DmesTemp, Dreel)]
plt.plot(np.array(Dreel), np.array(Erreur),
         color="y", label=r'$\epsilon$' + ' (avec Temp) (%)')
plt.plot(np.array(Dreel), [np.average(Erreur)] * len(Dreel),
         color="b", label=r'$\epsilon$' + ' moyen (avec Temp) (%)')
plt.xlabel(xlabel)
plt.ylabel(ylabel)
plt.title(title)
plt.grid(True)
plt.text(275, 2, r'$\epsilon$' + '= '+str(round(np.average(Erreur), 2))+'%')
plt.legend(loc='upper right')
plt.savefig("graphes/"+title+" - 3m .png")
print('Graphe 2 Cree ! ✔')


plt.clf()
Erreur = [abs(v - u) / v * 100 for u, v in zip(Y, X)]

xlabel = 'Distance Réelle (cm)'  # ex : 'Axe des X'
ylabel = 'Erreur mesurée ' + r'$\epsilon$' + ' (%)'  # ex : 'Axe des Y'
title = 'Erreur en fonction de la distance mesure'  # ex : 'Titre du graphe'

plt.plot(np.array(X), np.array(Erreur),
         color="r", label=r'$\epsilon$' + ' (%)')
plt.plot(np.array(X), [np.average(Erreur)] * len(X),
         color="b", label=r'$\epsilon$' + ' moyen (%)')

plt.text(95, 7, r'$\epsilon$' + '= '+str(round(np.average(Erreur), 2))+'%')
plt.xlabel(xlabel)
plt.ylabel(ylabel)
plt.title(title)
plt.grid(True)
plt.legend(loc='upper right')
plt.savefig("graphes/"+title+" - 1m .png")
print('Graphe 3 Cree ! ✔')

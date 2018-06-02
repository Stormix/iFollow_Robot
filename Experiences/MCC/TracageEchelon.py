import serial
import numpy as np
from matplotlib import pyplot as plt
from time import time

# If you're not using Linux, you'll need to change this
# check the Arduino IDE to see what serial port it's attached to
ser = serial.Serial('COM7', 115200, timeout=0)

# set plot to animated

start_time = time()
timepoints = []

ydata = []
view_time = 4  # seconds of data to view at once
duration = 10  # total seconds to collect data

#plt.xlim([0, view_time])

# flush any junk left in the serial buffer
ser.flushInput()
# ser.reset_input_buffer() # for pyserial 3.0+
run = True

# collect the data and plot a moving frame
while run:
    ser.reset_input_buffer()
    data = ser.readline().decode("utf-8")
    if data != "":
        print(data)
        # sometimes the incoming data is garbage, so just 'try' to do this
        # store the entire dataset for later
        data = float(data)  # float(data)*5.0/1024
        ydata.append(data)
        timepoints.append(time()-start_time)
        current_time = timepoints[-1]

        # when time's up, kill the collect+plot loop
        if timepoints[-1] > duration:
            run = False

xlabel = 'Temps (.?)'  # ex : 'Axe des X'
ylabel = 'Vitesse (tr/min)'  # ex : 'Axe des Y'
title = ''  # ex : 'Titre du graphe'

print(ydata)
plt.plot(np.array(timepoints), np.array(ydata),
         color="c", label=ylabel)
plt.xlabel(xlabel)
plt.ylabel(ylabel)
plt.title(title)
plt.grid(True)
plt.legend(loc='lower right')
plt.savefig("image.png")
print('Graphe 0 Cree ! ✔')

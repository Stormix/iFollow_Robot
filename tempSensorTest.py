import sys
import Adafruit_DHT

while True:
    humidity, temperature = Adafruit_DHT.read_retry(11, 23)
    # https://fr.wikipedia.org/wiki/Vitesse_du_son
    SoundSpeed = (331.5 + 0.607 * temperature)
    print(SoundSpeed)

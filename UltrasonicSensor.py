"""
    Distance sensor module
    >_ Fetchs the distance mesured by the ultrasonic sensor
"""
import time
import RPi.GPIO as GPIO
import Adafruit_DHT
import IOSetup as IO


class distanceSensor:
    '''
        UltrasonicSensor as a distanceSensor class
    '''

    def __init__(self, ID, TRIGGER_PIN, ECHO_PIN, detectionDistance=5):

        self.ID = ID
        self.TRIGGER_PIN = TRIGGER_PIN
        self.ECHO_PIN = ECHO_PIN
        self.detectionDistance = detectionDistance
        self.TEMP_SENSOR = IO.TEMP_SENSOR
        GPIO.setup(self.TRIGGER_PIN, GPIO.OUT)
        GPIO.setup(self.ECHO_PIN, GPIO.IN)
        GPIO.output(self.TRIGGER_PIN, False)

    def __str__(self):

        return """ Ultrasonic Sensor {} mesuring {}""".format(self.ID, self.mesureDistance())

    def getSoundSpeed(self):
        humidity, temperature = Adafruit_DHT.read_retry(11, self.TEMP_SENSOR)
        # https://fr.wikipedia.org/wiki/Vitesse_du_son
        SoundSpeed = (331.5 + 0.607 * temperature)
        #print("Sound speed at {} degrees is : {}".format(SoundSpeed,temperature))
        return SoundSpeed

    def mesureDistance(self, MesureTemp=False):
        """
            Mesures the distance as detailed in the Datasheet
            return: float : distance in cm
        """
        # time.sleep(1)
        #print('La distance de mesure en progression')
        # on a besoin d'un pulsation de LARGEUR 10microseconde
        GPIO.output(self.TRIGGER_PIN, True)
        time.sleep(0.000001)
        GPIO.output(self.TRIGGER_PIN, False)
        while GPIO.input(self.ECHO_PIN) == 0:
            start = time.time()
        while GPIO.input(self.ECHO_PIN) == 1:
            end = time.time()
        # le temps divise par deux car la variation mesure la double distance
        Time = (end - start) / 2
        Velocity = 340 if not MesureTemp else self.getSoundSpeed()  # a 20 deg celsius
        distance = round(float(Time * Velocity * 100), 2)
        return distance

    def isObstacleDetected(self):
        return self.mesureDistance() <= self.detectionDistance

"""
    Distance sensor module
    >_ Fetchs the distance mesured by the ultrasonic sensor
"""
import time
import RPi.GPIO as GPIO


class UltrasonicSensor:
    '''
        UltrasonicSensor class
    '''

    def __init__(self, ID, TRIGGER_PIN, ECHO_PIN):

        self.ID = ID
        self.TRIGGER_PIN = TRIGGER_PIN
        self.ECHO_PIN = ECHO_PIN

        GPIO.setup(self.TRIGGER_PIN, GPIO.OUT)
        GPIO.setup(self.ECHO_PIN, GPIO.IN)
        GPIO.output(self.TRIGGER_PIN, False)

    def __str__(self):

        return """ Ultrasonic Sensor {} mesuring {}""".format(self.ID, self.mesureDistance())

    def mesureDistance(self):
        """
            Mesures the distance as detailed in the Datasheet
            return: float : distance in cm
        """
        time.sleep(1)
        #print('La distance de mesure en progression')
        # on a besoin d'un pulsation de LARGEUR 10microseconde
        GPIO.output(self.TRIGGER_PIN, True)
        time.sleep(0.000001)
        GPIO.output(self.TRIGGER_PIN, False)

        while GPIO.input(self.ECHO_PIN) == 0:
            start = time.time()
        while GPIO.input(self.ECHO_PIN) == 1:
            end = time.time()
        # le temps divisé par deux car la variation mesure la double distance
        Time = (end - start) / 2
        Velocity = 343 * 100  # à 25 deg celsius
        distance = round(float(Time * Velocity), 2)
        GPIO.cleanup()
        return distance

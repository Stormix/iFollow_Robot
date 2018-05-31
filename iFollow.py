"""
      _ _____     _ _                 ____       _           _
     (_)  ___|__ | | | _____      __ |  _ \ ___ | |__   ___ | |_
     | | |_ / _ \| | |/ _ \ \ /\ / / | |_) / _ \| '_ \ / _ \| __|
     | |  _| (_) | | | (_) \ V  V /  |  _ < (_) | |_) | (_) | |_
     |_|_|  \___/|_|_|\___/ \_/\_/   |_| \_\___/|_.__/ \___/ \__|

    iFollow - TIPE PROJECT
    @Authors : Anas Mazouni & Ismail Ouadrhiri
    @Date:   2017-06-07
    @Project: iFollow
    @Last modified time: 2018-03-30
"""

from UltrasonicSensor import distanceSensor
import Math
from servoMotor import servoMotor
import IOSetup as IO
from motor import DCMotor as Motor
from time import sleep

#import colorTracker


class iFollow:
    '''
        iFollow robot class
    '''
    def __init__(self):

        self.UltrasonicSensors = {
            "ObstacleSensor" : UltrasonicSensor("Obstacle", IO.TRIG1, IO.ECHO1)
            "DistanceSensor" : UltrasonicSensor("Distance", IO.TRIG2, IO.ECHO2)
        }
        self.Motors = {
            "LEFT" : Motor("LEFT", IO.MOTOR_L_X, IO.MOTOR_L_X)
            "RIGHT" : Motor("RIGHT", IO.MOTOR_R_X, IO.MOTOR_R_X)
        }
        self.servoMotor = servoMotor(0, IO.SERVO)
        self.status = "Running"
        # Camera resolution
        self.cameraHeight = 800
        self.cameraWidth = 600
        # Servo Angle Steps
        self.Step = 10
        # Vitesse Consigne
        self.setSpeed = 50
        # Obstacle detection distance limit, an Obstacle will be considered
        # detected if the separating distance is less than it.
        self.detectionDistance = 3
        self.setTrackingEps = 2 # Erreur accepte

    def __str__(self):
        '''
            Object Representation
        '''
        distance = self.UltrasonicSensors["DistanceSensor"].mesureDistance()
        obstacle = self.UltrasonicSensors["ObstacleSensor"].isObstacleDetected()
        motorL = self.Motors["LEFT"].status
        motorR = self.Motors["RIGHT"].status
        servoAngle = self.servoMotor.lastAngle
        # Running, Following, Disabled
        return """
                      _ _____     _ _                 ____       _           _
                     (_)  ___|__ | | | _____      __ |  _ \ ___ | |__   ___ | |_
                     | | |_ / _ \| | |/ _ \ \ /\ / / | |_) / _ \| '_ \ / _ \| __|
                     | |  _| (_) | | | (_) \ V  V /  |  _ < (_) | |_) | (_) | |_
                     |_|_|  \___/|_|_|\___/ \_/\_/   |_| \_\___/|_.__/ \___/ \__|

                        > Status : {}
                        > Sensors :
                                Distance Sensor : {} cm
                                Obstacle Sensor : {}
                        > Servo Angle : {} degree
                        > Camera :
                                Object (not) detected
                        > Motors :
                            Motor Left: {}
                            Motor Right: {}
                """.format(self.status, distance, obstacle,  servoAngle,  motorL,  motorR)

    def trackPerson(self, *args):
        x = 0
        y = 0
        return x, y

    def detectObstacle(self):
        """
            We're using a the seconds sensor to detect obstacles
        """
        return self.UltrasonicSensors["ObstacleSensor"].isObstacleDetected()

    def followDirection(self):
        x,y = self.trackPerson() # Get tracked object center coordinates
        servoMaxAngle = self.servoMotor.maxAngle
        Step = self.Step
        while x > self.setTrackingEps:
            # Currently outside the tracking premise
            #self.setXCoordinates(x)
            servoCurrentAngle = self.servoMotor.lastAngle
            setAngle = servoCurrentAngle
            distance = self.UltrasonicSensors["DistanceSensor"].mesureDistance()
            angle = Math.arcsin(x/distance)
            # Rotate the servo motor to the calculated angle
            setAngle += angle
            self.servoMotor.setServoAngle(setAngle)
            sleep(100) # update after 100ms

    def followPerson(self):
        x, y = self.trackPerson()
        pass

    def shutdown(self):
        #Stop everyting & cleanup
        GPIO.cleanup()

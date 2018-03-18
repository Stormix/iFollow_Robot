"""
    iFollow - TIPE PROJECT
    @Authors : Anas Mazouni & Ismail Ouadrhiri
    @Date:   2017-06-07
    @Project: iFollow
    @Last modified time: 2018-03-18
"""

import controller
import distanceSensor.UltrasonicSensor as UltrasonicSensor
import servoMotor.servoMotor as servoMotor
import IOSetup as IO
import Interface.main.Interface as Interface
import motor.DCMotor as Motor
#import colorTracker


class iFollow:
    '''
        iFollow robot class
    '''
    def __init__():

        self.UltrasonicSensors = [UltrasonicSensor(0, IO.TRIG1, IO.ECHO1), UltrasonicSensor(1, IO.TRIG2, IO.ECHO2)]
        self.Motors = [Motor(0, IO.MOTOR_L_X, IO.MOTOR_L_X), Motor(1, IO.MOTOR_R_X, IO.MOTOR_R_X)]
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

    def __str__(self):
        '''
            Object Representation
        '''
        distance1 = self.UltrasonicSensors[0].mesuredistance()
        distance2 = self.UltrasonicSensors[1].mesuredistance()
        motorL = self.Motors[0].status
        motorR = self.Motors[1].status
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
                                Sensor 1 : {} cm
                                Sensor 2 : {} cm
                        > Servo Angle : {}°
                        > Camera :
                                Object (not) detected
                        > Motors :
                            Motor Left: {}
                            Motor Right: {}
                """.format(self.status, distance1, distance2,  servoAngle,  motorL,  motorR)

    def trackPerson(self, *args):
        x = 0
        y = 0
        return x, y

    def detectObstacle(self):
        """
            We're using a the seconds sensor to detect obstacles
        """
        mesuredDistance = self.UltrasonicSensors[1].mesuredistance()
        return mesuredistance <= self.detectionDistance

    def panCamera(self, x):
        centerCoordinates = (self.cameraWidth / 2, self.cameraHeight / 2)
        centerXCoordinate = centerCoordinates[0]
        servoMaxAngle = self.servoMotor.maxAngle
        servoCurrentAngle = self.servoMotor.lastAngle
        Step = self.Step
        setAngle = servoCurrentAngle

        if (x < centerXCoordinate):
            setAngle += Step
            if setAngle > servoMaxAngle:
                setAngle = servoMaxAngle
            print("Rotating to : {}°, Last angle was : {}°, Step Angle : {}°".format(
                setAngle, servoCurrentAngle, Step))
        if (x > centerXCoordinate):
            setAngle -= Step
            if setAngle < 0:
                setAngle = 0  # Minimum possible angle is 0°
            print("Rotating to : {}°, Last angle was : {}°, Step Angle : {}°".format(
                setAngle, servoCurrentAngle, Step))

    def followPerson(self):
        x, y = self.trackPerson():
        pass

    def shutdown(self):
        #Stop everyting & cleanup
        GPIO.cleanup()

"""
    Import flask lib & Controls module
"""

from flask import Flask, render_template, json
import random, math
import iFollow.iFollow as iFollow
import chassis as Chassis

"""
    Initiate the Flask app
"""
app = Flask(__name__)

@app.route("/")
def main():
    """
        If we visit pi_ip:5000/ - Render the dashboard
    """
    return render_template('index.html')

@app.route("/data")
def getData():
    """
        If we visit pi_ip:5000/data - Output data as Json
    """
	iFollowRobot = iFollow()
    status = 1 if iFollowRobot.status == "Running" else 0

    # Rotational speed
    leftMotorSpeed = 10.0
    rightMotorSpeed = 10.0

    # Lineaire speed V = Omega * Radius and Omega = 2 * pi * motorSpeed /60
    leftMotorSpeedLin = ((2 * math.pi * leftMotorSpeed ) / 60 ) *  Chassis.rayonRoue
    rightMotorSpeedLin = ((2 * math.pi * rightMotorSpeed ) / 60 ) *  Chassis.rayonRoue

    # Distance mesuree
    distance = iFollowRobot.UltrasonicSensors[0].mesuredistance()
    distance2 = iFollowRobot.UltrasonicSensors[1].mesuredistance()

    #Motors status
    motorL = self.Motors[0].status
    motorR = self.Motors[1].status

    data = {
            'etat': status , # Arrêt 0 / Marche 1,
            'vitesse_mes_gauche': round(leftMotorSpeed,2), # Vitesse Moteur Gauche : 20 tr/min
            'vitesse_mes_droit' : round(rightMotorSpeed,2), # Vitesse Moteur Droit : 20 tr/min
            'vitesse_consigne' : iFollowRobot.setSpeed,
            'vitesse_lineaire_gauche': round(leftMotorSpeedLin,2), # Vitesse lineaire Gauche : 20 m/s
            'vitesse_lineaire_droit' : round(rightMotorSpeedLin,2), # Vitesse lineaire Droit : 20 m/s
            'distance_mes_gauche': round(distance1,2), # Distance gauche : 10 cm
            'distance_mes_droit' : round(random.uniform(1, 30),2), # Distance Droit : 30 cm
            'distance_consigne' : 10,
            'etat_M_L' : motorL, # Arrêt 0 / Marche 1,
            'etat_M_R' : motorR, # Arrêt 0 / Marche 1
           }
    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    return response # Output data in json format (text python dictionary)


if __name__ == "__main__":
    app.run()

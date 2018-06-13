"""
    Import flask lib & Controls module
"""

from flask import Flask, render_template, json
import random
import math

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


if __name__ == "__main__":
    app.run(debug=True, port=5000, host='0.0.0.0')

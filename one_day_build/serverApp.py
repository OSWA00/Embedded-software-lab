import json
import time
from flask import Flask
from flask import request, jsonify, render_template
import grovepi
from grove_rgb_lcd import *

# Connect the Grove Light Sensor to analog port A0
# SIG,NC,VCC,GND
light_sensor = 0

# Connect the LED to digital port D4
# SIG,NC,VCC,GND
led = 4

# Turn on LED once sensor exceeds threshold percentage
threshold = 10

# Set pins modes
grovepi.pinMode(light_sensor,"INPUT")
grovepi.pinMode(led,"OUTPUT")

# Set blackligth of the LCD
setRGB(0,0,255)

app = Flask(__name__, template_folder='templates')

sensors = {
        "light":{
            "level":0, 
            "ref"  :0
        }
}

actuators = {
        "LED":{
            "state":0,
            "mode" :0
        }
}

@app.route("/")
def home():
    # Read sensor status
    sensor_value = grovepi.analogRead(light_sensor)
    lightStats = (float)(sensor_value) / 1023 * 100
    sensors["light"]["level"] = "%.1f" %(lightStats)
    setText_norefresh("Light level:" + sensors["light"]["level"]) # LCD
    template_data = {
        'light_lev': sensors["light"]["level"],
        'led_stat' : actuators["LED"]["state"]
    }
    return render_template('home.html', **template_data)

@app.route("/about")
def about():
    return '''This system allows the user to monitor sensors
              and modify some basic smart home configurations'''

@app.route('/api/sensors/light/',methods=['GET'])
def getSensor():
    setText_norefresh("Light level:" + sensors["light"]["level"])
    sensor_value = grovepi.analogRead(light_sensor)
    lightStats = (float)(sensor_value) / 1023 * 100
    sensors["light"]["level"] = "%.1f" %(lightStats)
    template_data = {
        'light_lev': sensors["light"]["level"],
        'led_stat' : actuators["LED"]["state"]
    }
    return render_template('home.html', **template_data)


@app.route('/api/actuators/LED/',methods=['GET'])
def getActuator():
    setText_norefresh("Light level:" + sensors["light"]["level"])
    template_data = {
    'light_lev': sensors["light"]["level"],
    'led_stat' : actuators["LED"]["state"]
    }
    return render_template('home.html',**template_data)


@app.route('/api/sensors/light/ref', methods=['PATCH'])
def update_ref():
    global threshold
    try:
        request_data = request.get_json()
        if (request_data.isnumeric()):
            sensors["light"]['ref'] = request_data['ref']
            threshold = int(sensors["light"]['ref'])
        return jsonify(sensors)
    except KeyError:
        return json.dumps({'message': 'Sensor not found'})

@app.route('/api/actuators/LED/mode', methods=['PATCH'])
def update_mode():
    try:
        request_data = request.form['mode']
        if (request_data.isnumeric()):
            actuators["LED"]["mode"] = int(request_data)
            if (actuators["LED"]['mode'] == 1):
                grovepi.digitalWrite(led, 1) #! Change hardware function
            elif (actuators["LED"]['mode'] == 0):
                grovepi.digitalWrite(led, 0) #! Change hardware function
        actuators["LED"]['mode'] = request_data['mode']
        setText_norefresh("Light level:" + sensors["light"]["level"])
        return jsonify(actuators)
    except KeyError:
        return json.dumps({'message': 'Actuator not found'})


@app.route('/api/actuators/LED/state/', methods=['POST'])
def update_state():
    request_data = request.form['state']
    if (request_data.isnumeric()):
        actuators["LED"]['state'] = int(request_data)
        if (actuators["LED"]['state'] == 1):
            grovepi.digitalWrite(led, 1)
        elif (actuators["LED"]['state'] == 0):
            grovepi.digitalWrite(led, 0)
    setText_norefresh("Light level:" + sensors["light"]["level"])
    template_data = {
        'light_lev': sensors["light"]["level"],
        'led_stat' : actuators["LED"]["state"]
    }
    return render_template('home.html',**template_data)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)



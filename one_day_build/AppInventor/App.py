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
    "light":{"level":0, "ref"  :0}
}

actuators = {
        "Led":{
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
    setText_norefresh("Light level:" + sensors["light"]["level"])
    return render_template('home.html', **sensors)

@app.route("/about")
def about():
    return '''This system allows the user to monitor sensors
              and modify some basic smart home configurations'''

@app.route('/api/sensors/<sen_type>/',methods=['GET'])
def getSensor(sen_type):
    try:
        sensor_value = grovepi.analogRead(light_sensor)
        lightStats = (float)(sensor_value) / 1023 * 100
        sensors[sen_type]["level"] = "%.1f" %(lightStats)
        setText_norefresh("Light level:" + sensors[sen_type]["level"])
        return jsonify(sensors[sen_type])
    except KeyError:
        return sen_type + " sensor" + "Not Found"

@app.route('/api/actuators/<act_type>/',methods=['GET'])
def getActuator(act_type):
    try:
        print(actuators[act_type])
        return jsonify(actuators[act_type])
    except KeyError:
        return act_type + "'s " + atrib + "Not Found"


@app.route('/api/sensors/<sen_type>/ref', methods=['PATCH'])
def update_ref(sen_type):
    global threshold
    try:
        request_data = request.get_json()
        if (request_data.isnumeric()):
            sensors[sen_type]['ref'] = request_data['ref']
            threshold = int(sensors[sen_type]['ref'])
        return jsonify(sensors)
    except KeyError:
        return json.dumps({'message': 'Sensor not found'})

@app.route('/api/actuators/<act_type>/mode', methods=['PATCH'])
def update_mode(act_type):
    try:
        request_data = request.get_json()
        actuators[act_type]['mode'] = request_data['mode']
        setText_norefresh("Light level:" + sensors["light"]["level"])
        return jsonify(actuators)
    except KeyError:
        return json.dumps({'message': 'Actuator not found'})


@app.route('/api/actuators/<act_type>/state', methods=['PUT'])
def update_state(act_type):
    try:
        request_data = request.get_json()
        print(request_data)
        actuators[act_type]['state'] = request_data['state']
        if (actuators[act_type]['state'] == '1'):
            grovepi.digitalWrite(led, 1)
        elif (actuators[act_type]['state'] == '0'):
            grovepi.digitalWrite(led, 0)
        return jsonify(actuators[act_type])
    except KeyError:
        return json.dumps({'message': 'Actuator not found'})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

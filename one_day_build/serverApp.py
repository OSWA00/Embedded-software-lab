import json
from flask import Flask
from flask import request, jsonify

app = Flask(__name__)

sensors = [
    {
        "Light":{
            "level":0, 
            "ref"  :0
        }
    }
]

actuators = [
    {
        "Led":{
            "state":0,
            "mode" :0
        }
    }
]

@app.route("/")
def hello():
    return "Smart Home monitoring app"

@app.route("/about")
def about():
    return '''This system allows the user to monitor sensors
              and modify some basic smart home configurations'''

@app.route('/api/sensors/<sen_type>/',methods=['GET'])
def getSensor(sen_type):
    try:
        return jsonify(sensors[sen_type])
    except KeyError:
        return sen_type + " sensor" + "Not Found"

@app.route('/api/actuators/<act_type>/',methods=['GET'])
def getActuator(act_type, atrib):
    try:
        return jsonify(actuators[act_type])
    except KeyError:
        return act_type + "'s " + atrib + "Not Found"

@app.route('/api/sensors/',methods=['POST'])
def createSensor():
    request_data = request.get_json()
    sensors.append(request_data)
    return jsonify( request_data )

@app.route('/api/actuators/',methods=['POST'])
def createActuator():
    request_data = request.get_json()
    actuators.append(request_data)
    return jsonify( request_data )

@app.route('/api/sensors/<sen_type>/ref', methods=['PUT'])
def update_ref(sen_type):
    try:
        request_data = request.get_json()
        sensors[sen_type]['ref'] = request_data['ref']
        return jsonify(sensors)
    except KeyError:
        return json.dumps({'message': 'Sensor not found'})

@app.route('/api/actuators/<act_type>/mode', methods=['PUT'])
def update_mode(act_type):
    try:
        request_data = request.get_json()
        actuators[act_type]['mode'] = request_data['mode']
        return jsonify(actuators)
    except KeyError:
        return json.dumps({'message': 'Actuator not found'})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

from flask import Flask, request, send_from_directory, jsonify
import json
from shapely.geometry import Point, Polygon

app = Flask(__name__)

fileName = '/Users/sammorrow/Desktop/untitled1/challenge/vehicles-location.json'


@app.route('/')
def hello_world():
    app.logger.error('Processing default request')
    return send_from_directory('static', 'index.html')


@app.route('/api/return_locations_in_polygon', methods=['POST'])
def return_locations_in_polygon():
    data = request.json
    vehicleData = []
    try:
        with open(fileName) as f:
            vehiclesSelect = json.loads(f.read())
        dataReceived = json.dumps(data)
        dataReceived = dataReceived[17:len(dataReceived) - 2]
        tuples = [tuple(float(y) for y in x.split(",")) for x in
                  dataReceived.split(" , ")]
        polygon = Polygon(tuples)
        for i in range(0, len(vehiclesSelect)):
            p = Point(vehiclesSelect[i].get('location').get('lat'),
                      vehiclesSelect[i].get('location').get('lng'))
            if polygon.contains(p):
                vehicleData.append(vehiclesSelect[i])
        return jsonify(vehicleData)
    except IOError:
        print("polygon error reached")


@app.route('/api/return_all_locations', methods=['POST'])
def return_all_locations():
    try:
        data = request.json
        vehicleData = []
        if data.get('status') == 'Show all vehicle locations':
            with open(fileName) as f:
                vehicleData = json.loads(f.read())
        else:
            print("send valid request")
        return jsonify(vehicleData)
    except EOFError:
        print(EOFError)


if __name__ == '__main__':
    app.run()

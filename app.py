from flask import Flask, request, send_from_directory, jsonify
import json
from shapely.geometry import Point, Polygon
from shapely.wkt import loads as load_wkt

app = Flask(__name__)

fileName = './vehicles-location.json'


@app.route('/')
def hello_world():
    app.logger.error('Processing default request')
    return send_from_directory('static', 'index.html')


@app.route('/api/return_locations_in_polygon', methods=['POST'])
def return_locations_in_polygon():
    data = request.json
    vehicleData = []
    with open(fileName) as f:
        vehiclesSelect = json.loads(f.read())
    polygon = load_wkt(data['shape'])
    for i in range(0, len(vehiclesSelect)):
        p = Point(vehiclesSelect[i].get('location').get('lng'),
                  vehiclesSelect[i].get('location').get('lat'))
        if polygon.contains(p):
            vehicleData.append(vehiclesSelect[i])
    return jsonify(vehicleData)


@app.route('/api/return_all_locations', methods=['POST'])
def return_all_locations():
    data = request.json
    vehicleData = []
    if data.get('status') == 'Show all vehicle locations':
        with open(fileName) as f:
            vehicleData = json.loads(f.read())
    else:
        print("send valid request")
    return jsonify(vehicleData)


if __name__ == '__main__':
    app.run()

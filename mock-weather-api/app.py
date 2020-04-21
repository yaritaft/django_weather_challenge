import os
import json
from flask import Flask, request, make_response
app = Flask(__name__)

ACCUWEATHER = None
NOAA = None
WEATHERDOTCOM = None

@app.route('/accuweather', methods=['GET'])
def accuweather():
    latitude_param, longitude_param = 'latitude', 'longitude'
    try:
        # validate that the user provided 'latitude' and 'longitude' as separate float values
        lat, lon = float(request.args.get(latitude_param)), float(request.args.get(longitude_param))
    except:
        return make_response('Must provide the "{:s}" and "{:s}" query params as float values\n'.format(latitude_param, longitude_param), 400)
    return json.dumps(ACCUWEATHER, indent=2)

@app.route('/noaa', methods=['GET'])
def noaa():
    param_name = 'latlon'
    try:
        # validate that the user provided the 'latlon' param as comma-separated floats
        lat, lon = map(float, request.args.get(param_name).split(','))
    except:
        return make_response('Must provide the "{:s}" query parameter in the form "30.2335595,-97.7797051"\n'.format(param_name), 400)
    return json.dumps(NOAA, indent=2)

@app.route('/weatherdotcom', methods=['POST'])
def weatherdotcom():
    try:
        # validate that the user provided the 'lat' and 'lon' params in a JSON body
        lat_param, lon_param = 'lat', 'lon'
        json_data = request.get_json()
        lat = float(json_data[lat_param])
        lon = float(json_data[lon_param])
    except:
        return make_response('Must provide the "{:s}" and "{:s}" query params as float values\n'.format(lat_param, lon_param), 400)
    return json.dumps(WEATHERDOTCOM, indent=2)


data_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data')

with open(os.path.join(data_path, 'accuweather.json'), 'r') as f:
    ACCUWEATHER = json.load(f)

with open(os.path.join(data_path, 'noaa.json'), 'r') as f:
    NOAA = json.load(f)

with open(os.path.join(data_path, 'weatherdotcom.json'), 'r') as f:
    WEATHERDOTCOM = json.load(f)

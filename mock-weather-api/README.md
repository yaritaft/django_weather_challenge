# mock-weather-api
Mock API for getting weather data

### Setup
```
virtualenv env
source env/bin/activate
pip install -r requirements.txt
FLASK_APP=app.py flask run
```

### Routes
Host: http://127.0.0.1:5000/
##### Accuweather
GET /accuweather?latitude=44&longitude=33

##### NOAA
GET /noaa?latlon=44,33

##### Weather.com
POST /weatherdotcom
{"lat":33.3,"lon":44.4}


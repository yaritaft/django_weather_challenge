# Django weather challenge

## Author

Yari Ivan Taft

- GitHub: http://github.com/yaritaft
- Website: http://yaritaft.com
- LinkedIn: https://www.linkedin.com/in/yari-ivan-taft-4122a7153/

## Summary

The app receives three inputs: latitude, longitude and a list of selected services to query.
Every external service is queried to gather the current temperature in those coordinates.
Then an average is calculated in Fahrenheit unit and that result will be shown in the frontend.

## Routes

http://127.0.0.1:8000/

## Dependencies

Dependencies may be found in requirements.txt.

## Pre-requisites

- Docker and docker compose installed.
- Docker and docker compose working without sudo.
- Python3 installed
- Pip3 installed
- Linux/Mac terminal (Or emulated linux in Windows)
- No services running on localhost port 8000 or 5000.

## Setup

1) First go with a terminal to this folder: mock-weather-api and type this:
```
virtualenv env
source env/bin/activate
pip install -r requirements.txt
FLASK_APP=app.py flask run
```

2) Open another terminal and go to repository's root folder. And type:
```
docker-compose build
docker-compose up
```

3) Open your browser and enter this url: http://127.0.0.1:8000 and you will be able to use the APP.

4) To shutdown the app type:
```
docker-compose down
```
And return to your first terminal the mock-weather-api running and press: Control + C

## Decisions made

1) It was not neccesary to persist data so no models or databases were used.
2) Each url is set as env variables to split prod and development endpoints.

## Assumptions

1) According to my research latitude and longitude can go from -180 to 180. So those are the boundaries and only 2 decimal places can be sent.
2) The average temperature is between current temperature of each external service.
3) The return value desired is an int value.
4) If no service is selected then an error message should be shown on the front end.
5) Temperature is expected in Fahrenheit units, since is the only unit shared between three services.
5) Because of the payload from weather dot com I assume that a celsius temperature may be returned. For that reason I applied a convertion to make it Fahrenheit.
6) The request should be shown synchronously, as soon as data is available.

## Tests

## Coverage

## Standards applied

- Flake8
- Black formatting
- PEP8
- PEP256

## Technologies applied

- Django
- Flask
- Docker
- Docker-compose
- Gunicorn

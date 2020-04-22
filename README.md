# Django weather challenge

## Author

Yari Ivan Taft

- GITHUB: http://github.com/yaritaft
- WEBSITE: http://yaritaft.com
- LINKEDIN: https://www.linkedin.com/in/yari-ivan-taft-4122a7153/

## Summary

The app receives three inputs, latitude, longitude, and a list of selected services to query.
Every external service is queried and an average is calculated in Fahrenheit units with the
current temperature of each external service.

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

2) Open another terminal and go to repositorie's root folder. And type:
```
docker-compose build
docker-compose up
```

3) Open your browser in this url: http://127.0.0.1:8000 and you will be able to use the APP.

4) To shutdown the app type:
```
docker-compose down
```
And return to your first terminal the mock-weather-api running and press: Control + C

## Decisions made

1) It was not neccesary to persist data so no models or databases were used.
2) Each url will be set as env variables for testing purposes.

## Assumptions

1) According to my research latitude and longitude can go from -180 to 180. So those are the boundaries.
2) The average is between current temp of each service.
3) The return value desired is an int value.
4) If no service is selected then an error should be raised in the front end.
5) Temperature is expected in Fahrenheit units, since is the only unit shared between three services.
5) Because of the payload from weather dot com I assume that a celsius temperature may be returned so in that case I applied a convertion to make it Fahrenheit.
6) The request should be shown synchronously.

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

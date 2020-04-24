# Django weather challenge

## Overview

The app receives three inputs: latitude, longitude and a list of selected services to query.
Every external service is queried to gather the current temperature in those coordinates.
Then an average is calculated in Fahrenheit unit and that result will be shown in the frontend.

## Author

Yari Ivan Taft

- GitHub: https://github.com/yaritaft
- Website: http://yaritaft.com
- LinkedIn: https://www.linkedin.com/in/yari-ivan-taft-4122a7153/

## Badges

[![Coverage Status](https://coveralls.io/repos/github/yaritaft/django_weather_challenge/badge.svg?branch=master)](https://coveralls.io/github/yaritaft/django_weather_challenge?branch=master)
[![Build Status](https://travis-ci.com/yaritaft/django_weather_challenge.svg?branch=master)](https://travis-ci.com/yaritaft/django_weather_challenge)

## Table of contents

- [Technology](#Technology)
- [Routes](#Routes)
- [PreRequisites](#Pre-requisites)
- [Setup](#Setup)
- [Tests and code coverage](#Tests-and-code-coverage)
- [Decisions Made](#Decisions-made)
- [Assumptions](#Assumptions)
- [Standards](#Standards)

## Technology

- Programming languaje: Python 3
- APP Framework: Django 3
- Mockservice Framework: Flask
- Containers: Docker, Docker-compose
- Web-server: Gunicorn

## Routes

Main URL: http://127.0.0.1:8000/

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
### How to run the APP

You have two way of running the App:
- Using docker-compose.
- Using your local python interpreter.

#### Docker
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
5) And return to your first terminal the mock-weather-api running and press: Control + C

#### Local python interpreter
2) Open another terminal and type:
```
python3 -m virtualenv -p python3 venv
source venv/bin/activate
pip install -r requirements.txt
gunicorn coderio.wsgi
```
3) Open your browser and enter this url: http://127.0.0.1:8000 and you will be able to use the APP.

4) To shutdown the app press control + C in the second terminal.

5) And return to your first terminal the mock-weather-api running and press: Control + C

#### Precommit install

Precommit hook is set. Every time you want to commit code, black will format the code and then Flake8 will check whether the code follows PEP8 standard or not. To install it in your project type inside virtualenv:

```
pre-commit install
```

## Tests and code coverage
Unit tests and integration tests were made. Integration tests only work with the API up and running.
Unit tests have their requests patched to avoid using the mock service.

Being in the virtualenv with dependencies installed and API up, type:

```
coverage run manage.py test
coverage report
```

In this way you will be able to check the code coverage.

Disclaimer: If the API is not up, only unit tests will work because the have their requests mocked.

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

## Standards

- Flake8
- Black formatting
- PEP8
- PEP256

# Django weather challenge

## Overview

The app receives three inputs: latitude, longitude and a list of selected services to query.
Every external service is queried to gather the current temperature in those coordinates.
Then an average is calculated in Fahrenheit unit and that result will be shown in the API response or frontend.

## Author

Yari Ivan Taft

- GitHub: https://github.com/yaritaft
- Website: http://yaritaft.com
- LinkedIn: https://www.linkedin.com/in/yari-ivan-taft-4122a7153/

## Badges

[![Build Status](https://travis-ci.org/yaritaft/django_weather_challenge.svg?branch=master)](https://travis-ci.org/yaritaft/django_weather_challenge)
[![Coverage Status](https://coveralls.io/repos/github/yaritaft/my_django_web_page/badge.svg?branch=master)](https://coveralls.io/github/yaritaft/my_django_web_page?branch=master)

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
- API Framework: Django rest framework (DRF)
- Mockservice Framework: Flask
- Containers: Docker, Docker-compose
- Web-server: Gunicorn

## Routes

- API endpoint: http://127.0.0.1:8000/api/
- API swagger: http://127.0.0.1:8000/swagger/
- Front-end URL: http://127.0.0.1:8000/

## Pre-requisites

- Docker and docker compose installed.
- Docker and docker compose working without sudo.
- Python3 installed
- Pip3 installed
- Linux/Mac terminal (Or emulated linux on Windows)
- No services running on localhost port 8000 or 5000.

## Setup

### How to run the APP

You have two way of running the App:
- Using docker-compose.
- Using your local python interpreter.

#### Docker
1) Open terminal in repository's root folder. And type:
```
docker-compose build
docker-compose up
```

2) Open your browser and enter this url: http://127.0.0.1:8000 and you will be able to use the APP.

3) Press Control + C and then type:
```
docker-compose down
```

#### Local python interpreter
1) First go with a terminal to this folder: mock-weather-api and type this:
```
virtualenv env
source env/bin/activate
pip install -r requirements.txt
FLASK_APP=app.py flask run
```

2) Open another terminal and type:
```
python3 -m virtualenv -p python3 venv
source venv/bin/activate
pip install -r requirements.txt
gunicorn coderio.wsgi
```
3) Open your browser and enter this url: http://127.0.0.1:8000 and you will be able to use the APP.

4) To shutdown the app press control + C on the second terminal.

5) And return to the first terminal with mock-weather-api running and press: Control + C

#### Precommit install

Precommit hook is set. Every time you want to commit code, black will format the code and then Flake8 will check whether the code follows PEP8 standard or not. To install it in your project type inside virtualenv:

```
pre-commit install
```

## How to use the API

When running the APP you can go to this URL with your browser: http://127.0.0.1:8000/swagger/
There you will be able to find how to make requests. You will also be able to test the API directly from there without having to use postman or curl.
Moreover inside weather/documentation/postman_collections there is a postman collection with examples of how to query the API to get different results.

## Tests and code coverage
Unit tests and integration tests were created. Integration tests only work with the API up and running.
Unit tests have their requests patched to avoid using the mock service.

Being in the virtualenv with dependencies installed and API up, type:

```
coverage run manage.py test
coverage report
```

In this way you will be able to check the code coverage.

Disclaimer: If the API is not up, only unit tests will work because they have their requests mocked.

## Decisions made

1) It was not neccesary to persist data, so no models or databases were used.
2) Each url is set as env variables to split production and development endpoints.

## Assumptions

1) According to the research made latitude and longitude can go from -180 to 180. So those are the boundaries and only 2 decimal places can be sent.
2) The average temperature is between current temperature of each external service.
3) The return value desired is an int value.
4) If no service is selected then an error message should be shown on the front end or api response.
5) Temperature is expected in Fahrenheit units, since it is the only unit shared between three services.
5) Because of the payload from weather dot com It was assumed that a celsius temperature may be returned. In that case a convertion is triggered to make it Fahrenheint.
6) The request should be shown synchronously, as soon as data is available.

## Standards

- PEP8
- PEP257
- Appnexus (google import order style)
- Flake8
- Flake8 Docstrings
- Flake8 Import Order
- Black formatting


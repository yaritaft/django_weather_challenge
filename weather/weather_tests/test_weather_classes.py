from django.http import HttpResponse
from django.test import TestCase, RequestFactory
import logging
import os
import requests
import mock
import json
from weather.exceptions import NotValidWeatherFormException


from weather.weather_classes import (
    AccuWeather,
    NoaaWeather,
    DotComWeather,
    AverageWeatherService,
)

logger = logging.getLogger(__name__)


class MyFakeSerivce:
    pass


def json_loader(file_path):
    root_test = os.path.dirname(__file__)
    file_path = os.path.join(root_test, file_path)
    with open(file_path, "r") as f:
        return json.load(f)


class TestAccuWeatherService(TestCase):
    def setUp(self):
        self.weather_service = AccuWeather()
        self.dict_mock_response = json_loader(
            "mock_responses/accuweather.json"
        )
        self.json_mock_response = json.dumps(self.dict_mock_response)
        self.request_response = HttpResponse(
            content=self.json_mock_response, status=200
        )

    def test_get_fahrenheit(self):
        result = self.weather_service._get_fahrenheit(self.dict_mock_response)
        self.assertEqual(result, 55)

    @mock.patch("weather.weather_classes.AccuWeather.request_external_api")
    def test_request_external_api(self, mock_response):
        mock_response.return_value = self.request_response
        response = self.weather_service.request_external_api(33, 44)
        self.assertEqual(response.status_code, 200)

    @mock.patch("weather.weather_classes.AccuWeather.request_external_api")
    def test_request_temp(self, mock_response):
        mock_response.return_value = self.request_response
        result = self.weather_service.request_temp(33, 44)
        self.assertEqual(result, 55)


class TestNoaaWeatherService(TestCase):
    def setUp(self):
        self.weather_service = NoaaWeather()
        self.dict_mock_response = json_loader("mock_responses/noaa.json")
        self.json_mock_response = json.dumps(self.dict_mock_response)
        self.request_response = HttpResponse(
            content=self.json_mock_response, status=200
        )

    def test_get_fahrenheit(self):
        result = self.weather_service._get_fahrenheit(self.dict_mock_response)
        self.assertEqual(result, 55)

    @mock.patch("weather.weather_classes.NoaaWeather.request_external_api")
    def test_request_external_api(self, mock_response):
        mock_response.return_value = self.request_response
        response = self.weather_service.request_external_api(33, 44)
        self.assertEqual(response.status_code, 200)

    @mock.patch("weather.weather_classes.NoaaWeather.request_external_api")
    def test_request_temp(self, mock_response):
        mock_response.return_value = self.request_response
        result = self.weather_service.request_temp(33, 44)
        self.assertEqual(result, 55)


class TestDotComWeatherService(TestCase):
    def setUp(self):
        self.weather_service = DotComWeather()
        self.dict_mock_response = json_loader(
            "mock_responses/weatherdotcom.json"
        )
        self.json_mock_response = json.dumps(self.dict_mock_response)
        self.request_response = HttpResponse(
            content=self.json_mock_response, status=200
        )

    def test_get_fahrenheit(self):
        result = self.weather_service._get_fahrenheit(self.dict_mock_response)
        self.assertEqual(result, 37)

    @mock.patch("weather.weather_classes.DotComWeather.request_external_api")
    def test_request_external_api(self, mock_response):
        mock_response.return_value = self.request_response
        response = self.weather_service.request_external_api(33, 44)
        self.assertEqual(response.status_code, 200)

    @mock.patch("weather.weather_classes.DotComWeather.request_external_api")
    def test_request_temp(self, mock_response):
        mock_response.return_value = self.request_response
        result = self.weather_service.request_temp(33, 44)
        self.assertEqual(result, 37)


class TestAverageWeatherService(TestCase):
    def setUp(self):
        self.weather_service = AverageWeatherService()
        self.tuple_1 = ("ACCUWEATHER",)
        self.tuple_2 = ("ACCUWEATHER", "NOAA")
        self.tuple_3 = ("ACCUWEATHER", "NOAA", "WEATHER_DOT_COM")
        self.tuple_4 = ("My fake service",)

    @mock.patch("weather.weather_classes.AccuWeather.request_external_api")
    @mock.patch("weather.weather_classes.NoaaWeather.request_external_api")
    @mock.patch("weather.weather_classes.DotComWeather.request_external_api")
    def test_average_temp_services(
        self, mock_response_dotcom, mock_response_noaa, mock_response_accu
    ):
        mock_response_dotcom.return_value = HttpResponse(
            content=json.dumps(
                json_loader("mock_responses/weatherdotcom.json")
            )
        )
        mock_response_noaa.return_value = HttpResponse(
            content=json.dumps(json_loader("mock_responses/noaa.json"))
        )
        mock_response_accu.return_value = HttpResponse(
            content=json.dumps(json_loader("mock_responses/accuweather.json"))
        )
        response_1 = self.weather_service.average_temp_services(
            self.tuple_1, 33, 44
        )
        response_2 = self.weather_service.average_temp_services(
            self.tuple_2, 33, 44
        )
        response_3 = self.weather_service.average_temp_services(
            self.tuple_3, 33, 44
        )
        self.assertEqual(response_1, 55)
        self.assertEqual(response_2, 55)
        self.assertEqual(response_3, 49)

    def test_average_temp_services_error(self):
        self.assertRaises
        (
            NotValidWeatherFormException,
            self.weather_service.average_temp_services,
            self.tuple_4,
            33,
            44,
        )

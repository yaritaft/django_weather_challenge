from django.http import HttpResponse
from django.test import TestCase, RequestFactory
import logging
import os
import requests
import mock
import json
from marshmallow.exceptions import ValidationError

from weather.weather_classes import AverageWeatherService

logger = logging.getLogger(__name__)


class TestIntegrationAverageWeatherService(TestCase):
    def setUp(self):
        self.weather_service = AverageWeatherService()
        self.tuple_1 = ("ACCUWEATHER",)
        self.tuple_2 = ("ACCUWEATHER", "NOAA")
        self.tuple_3 = ("ACCUWEATHER", "NOAA", "WEATHER_DOT_COM")

    def test_integration_average_temp_services(self):
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

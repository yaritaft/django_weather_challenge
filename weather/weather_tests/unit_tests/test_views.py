from django.http import HttpResponse
from django.test import TestCase, RequestFactory
from weather.exceptions import (
    ExternalServiceException,
    MissingFieldsException,
    NotValidServicesException,
)
import json

import mock


class TestWeatherView(TestCase):
    def setUp(self):
        self.not_valid_service_message = (
            "There is a not valid service or no services were provided."
        )

    def test_get_weather_view(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_post_weather_view_ok(self):
        response = self.client.post(
            "/", {"latitude": 33, "longitude": 44, "services": ["NOAA"]}
        )
        self.assertTemplateUsed(response, "weather/results.html")
        self.assertEqual(response.status_code, 200)

    def test_post_weather_view_empty_services(self):
        response = self.client.post(
            "/", {"latitude": 33, "longitude": 44, "services": []}
        )
        self.assertTemplateUsed(response, "weather/error_message.html")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.not_valid_service_message)

    def test_post_weather_view_without_latitude(self):
        """Multi dict key error exception will be triggered with this one."""
        response = self.client.post("/", {"latitude": 33, "services": []})
        self.assertTemplateUsed(response, "weather/error_message.html")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, MissingFieldsException.message)

    def test_post_weather_view_not_valid_external_service(self):
        response = self.client.post(
            "/",
            {"latitude": 33, "longitude": 44, "services": ["FAKE_SERVICE"]},
        )
        self.assertTemplateUsed(response, "weather/error_message.html")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.not_valid_service_message)

    def test_post_weather_view_missing_fields(self):
        response = self.client.post(
            "/", {"latitude": 33, "services": ["NOAA"]}
        )
        self.assertTemplateUsed(response, "weather/error_message.html")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, MissingFieldsException.message)

    @mock.patch("weather.weather_classes.requests.get")
    def test_post_weather_view_external_not_200_response(self, mock_request):
        mock_request.return_value = HttpResponse(status=404)
        response = self.client.post(
            "/", {"latitude": 33, "longitude": 44, "services": ["NOAA"]}
        )
        self.assertTemplateUsed(response, "weather/error_message.html")
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response, "There was an error requesting some external API."
        )

    @mock.patch("weather.weather_classes.requests.get")
    def test_post_weather_view_external_error_request(self, mock_request):
        mock_request.side_effect = Exception
        response = self.client.post(
            "/", {"latitude": 33, "longitude": 44, "services": ["NOAA"]}
        )
        self.assertTemplateUsed(response, "weather/error_message.html")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There was an error.")


class TestWeatherApiView(TestCase):
    def test_post_weather_view_api_ok(self):
        response = self.client.post(
            "/json/",
            {"latitude": 33, "longitude": 44, "services": ["NOAA"]},
            content_type="application/json",
        )
        content = json.loads(response.content)
        logging.exception(content)
        self.assertEqual(content["average_temp"], 55)
        self.assertEqual(response.status_code, 200)

    def test_post_weather_view_api_no_latitude(self):
        response = self.client.post(
            "/json/",
            {"longitude": 44, "services": ["NOAA"]},
            content_type="application/json",
        )
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(content["message"], MissingFieldsException.message)

    def test_post_weather_view_api_no_longitude(self):
        response = self.client.post(
            "/json/",
            {"latitude": 44, "services": ["NOAA"]},
            content_type="application/json",
        )
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(content["message"], MissingFieldsException.message)

    def test_post_weather_view_api_no_services(self):
        response = self.client.post(
            "/json/",
            {"latitude": 33, "longitude": 44, "services": []},
            content_type="application/json",
        )
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(content["message"], NotValidServicesException.message)

    def test_post_weather_view_api_wrong_services(self):
        response = self.client.post(
            "/json/",
            {"latitude": 33, "longitude": 44, "services": ["FakeService"]},
            content_type="application/json",
        )
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(content["message"], NotValidServicesException.message)

    def test_post_weather_view_api_wrong_type_services(self):
        response = self.client.post(
            "/json/",
            {"latitude": 33, "longitude": 44, "services": 33},
            content_type="application/json",
        )
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(content["message"], "There is an error.")

    def test_post_weather_view_api_missing_services(self):
        response = self.client.post(
            "/json/",
            {"latitude": 33, "longitude": 44},
            content_type="application/json",
        )
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(content["message"], NotValidServicesException.message)

    @mock.patch("weather.weather_classes.requests.get")
    def test_post_weather_view_external_error_request(self, mock_request):
        mock_request.side_effect = ExternalServiceException
        response = self.client.post(
            "/json/",
            {"latitude": 33, "longitude": 44, "services": ["NOAA"]},
            content_type="application/json",
        )
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(content["message"], ExternalServiceException.message)

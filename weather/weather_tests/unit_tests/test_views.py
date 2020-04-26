from django.http import HttpResponse
from django.test import TestCase, RequestFactory
from marshmallow.exceptions import ValidationError

from weather.exceptions import ExternalServiceException
import json

import mock


class TestWeatherView(TestCase):
    def setUp(self):
        self.validation_error_message = "Some fields are not right."

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
        self.assertContains(response, self.validation_error_message)

    def test_post_weather_view_without_latitude(self):
        """Multi dict key error exception will be triggered with this one."""
        response = self.client.post("/", {"latitude": 33, "services": []})
        self.assertTemplateUsed(response, "weather/error_message.html")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.validation_error_message)

    def test_post_weather_view_not_valid_external_service(self):
        response = self.client.post(
            "/",
            {"latitude": 33, "longitude": 44, "services": ["FAKE_SERVICE"]},
        )
        self.assertTemplateUsed(response, "weather/error_message.html")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.validation_error_message)

    def test_post_weather_view_missing_fields(self):
        response = self.client.post(
            "/", {"latitude": 33, "services": ["NOAA"]}
        )
        self.assertTemplateUsed(response, "weather/error_message.html")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.validation_error_message)

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
    def setUp(self):
        self.validation_error_message = "Some fields are not right."

    def test_post_weather_view_api_ok(self):
        response = self.client.post(
            "/api/",
            {"latitude": 33, "longitude": 44, "services": ["NOAA"]},
            content_type="application/json",
        )
        content = json.loads(response.content)
        self.assertEqual(content["average_temp"], 55)
        self.assertEqual(response.status_code, 200)

    def test_post_weather_view_api_no_latitude(self):
        response = self.client.post(
            "/api/",
            {"longitude": 44, "services": ["NOAA"]},
            content_type="application/json",
        )
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(content["message"], self.validation_error_message)

    def test_post_weather_view_api_no_longitude(self):
        response = self.client.post(
            "/api/",
            {"latitude": 44, "services": ["NOAA"]},
            content_type="application/json",
        )
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(content["message"], self.validation_error_message)

    def test_post_weather_view_api_no_services(self):
        response = self.client.post(
            "/api/",
            {"latitude": 33, "longitude": 44, "services": []},
            content_type="application/json",
        )
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(content["message"], self.validation_error_message)

    def test_post_weather_view_api_wrong_services(self):
        response = self.client.post(
            "/api/",
            {"latitude": 33, "longitude": 44, "services": ["FakeService"]},
            content_type="application/json",
        )
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(content["message"], self.validation_error_message)

    def test_post_weather_view_api_wrong_type_services(self):
        response = self.client.post(
            "/api/",
            {"latitude": 33, "longitude": 44, "services": 33},
            content_type="application/json",
        )
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(content["message"], self.validation_error_message)

    def test_post_weather_view_api_missing_services(self):
        response = self.client.post(
            "/api/",
            {"latitude": 33, "longitude": 44},
            content_type="application/json",
        )
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(content["message"], self.validation_error_message)

    @mock.patch("weather.weather_classes.requests.get")
    def test_post_weather_view_external_error_request(self, mock_request):
        mock_request.side_effect = ExternalServiceException
        response = self.client.post(
            "/api/",
            {"latitude": 33, "longitude": 44, "services": ["NOAA"]},
            content_type="application/json",
        )
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(content["message"], ExternalServiceException.message)

    @mock.patch("weather.weather_classes.len")
    def test_unknown_error(self, mock_request):
        mock_request.side_effect = TypeError
        response = self.client.post(
            "/api/", {"latitude": 33, "longitude": 44, "services": ["NOAA"]}
        )
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(content["message"], "There is an error.")

from django.http import HttpResponse
from django.test import TestCase, RequestFactory
import json

import mock


class TestWeatherView(TestCase):
    def setUp(self):
        self.not_valid_service_message = (
            "You did not select any service to query."
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
        self.assertContains(response, "Some field was not provided.")

    # @mock.patch("weather.weather_classes.NoaaWeather.request_external_api")
    # def test_post_weather_view_external_service_error_no_response(self, mock_response):
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
        self.assertContains(response, "Some field was not provided.")

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

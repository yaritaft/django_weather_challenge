from django.http import HttpResponse
from django.test import TestCase, RequestFactory


class TestWeatherView(TestCase):
    def test_get_weather_view(self):
        response = self.client.get("/")
        assert response.status_code == 200

    # def test_post_weather_view_ok(self):
    #     response = self.client.post(
    #         "/",
    #         {"latitude": 33, "longitude": 44, "services": ["NOAA"]}
    #     )
    # def test_post_weather_view_empty_services(self):
    #     response = self.client.post(
    #         "/",
    #         {"latitude": 33, "longitude": 44, "services": []}
    #     )
    def test_post_weather_view_without_latitude(self):
        """Multi dict key error exception will be triggered with this one."""
        response = self.client.post("/", {"latitude": 33, "services": []})
        assert response.status_code == 200

    # def test_post_weather_view(self):
    #     response = self.client.post(
    #         "/",
    #         {"latitude": 33, "longitude": 44, "services": []}
    #     )

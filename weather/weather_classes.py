import functools
import json
import logging
import os

import requests

from weather.exceptions import (
    ExternalServiceException,
    NotValidWeatherFormException,
)
from .validators import check_request_external_api


logger = logging.getLogger(__name__)


class WeatherService:
    """Abstract class to calculate the average temp using polymorphism.

    Return average temp with checked services with given latitude
    and longitude.
    """

    def request_temp(self, lat, lon):
        """Request temp to subclass service.

        Abstract method to request the subclass to request data,
        and parse it.

        Parameters
        ----------
        lat: float
            Latitude value. From -180 to 180.
        lon: float
            Longitude value. From -180 to 180.

        Returns
        -------
        int
            Current fahrenheit temperature for service queried.
        """
        response = self.request_external_api(lat, lon)
        return self.get_fahrenheit(json.loads(response.content))


class AccuWeather(WeatherService):
    """Accu weather service."""

    url = os.getenv("AccuWeather")
    service_key = "ACCUWEATHER"

    def get_fahrenheit(self, temp_data):
        """Get fahrenheit temperature from service.

        Parameters
        ----------
        temp_data: dict
            Temperature data from response content from API queried.

        Returns
        -------
        int
            Fahrenheit current temperature.
        """
        return int(
            temp_data["simpleforecast"]["forecastday"][0]["current"][
                "fahrenheit"
            ]
        )

    @check_request_external_api(logger)
    def request_external_api(self, lat, lon):
        """Request external API to provide weather data.

        Parameters
        ----------
        lat: float
            Latitude value. From -180 to 180.
        lon: float
            Longitude value. From -180 to 180.

        Returns
        -------
        HttpResponse
            Weather data from external API.
        """
        response = requests.get(
            self.url, params={"latitude": int(lat), "longitude": int(lon)}
        )
        return response


class NoaaWeather(WeatherService):
    """NOAA weather service."""

    url = os.getenv("NoaaWeather")
    service_key = "NOAA"

    def get_fahrenheit(self, temp_data):
        """Get fahrenheit temperature from service.

        Parameters
        ----------
        temp_data: dict
            Temperature data from response content from API queried.

        Returns
        -------
        int
            Fahrenheit current temperature.
        """
        return int(temp_data["today"]["current"]["fahrenheit"])

    @check_request_external_api(logger)
    def request_external_api(self, lat, lon):
        """Request external API to provide weather data.

        Parameters
        ----------
        lat: float
            Latitude value. From -180 to 180.
        lon: float
            Longitude value. From -180 to 180.

        Returns
        -------
        HttpResponse
            Weather data from external API.
        """
        lat_long = ",".join((str(lat), str(lon)))
        response = requests.get(self.url, params={"latlon": lat_long})
        return response


class DotComWeather(WeatherService):
    """Weather dot com service."""

    url = os.getenv("DotComWeather")
    service_key = "WEATHER_DOT_COM"

    def get_fahrenheit(self, temp_data):
        """Get fahrenheit temperature from service.

        Assumption: It have been assumed that if the unit is not Fahrenheit it
        will be Celsius so the convertion is applied.
        Formula: fahrenheit = (celsius° * 9/5) + 32

        Parameters
        ----------
        temp_data: dict
            Temperature data from response content from API queried.

        Returns
        -------
        int
            Fahrenheit current temperature.
        """
        temp = int(
            temp_data["query"]["results"]["channel"]["condition"]["temp"],
        )
        if (
            temp_data["query"]["results"]["channel"]["units"]["temperature"]
            == "F"
        ):
            return int(temp)
        else:
            return int(temp * (9 / 5)) + 32

    @check_request_external_api(logger)
    def request_external_api(self, lat, lon):
        """Request external API to provide weather data.

        Parameters
        ----------
        lat: float
            Latitude value. From -180 to 180.
        lon: float
            Longitude value. From -180 to 180.

        Returns
        -------
        HttpResponse
            Weather data from external API.
        """
        response = requests.post(
            self.url, json={"lat": float(lat), "lon": float(lon)},
        )
        return response


class AverageWeatherService:
    """Average weather service."""

    subclasses = WeatherService.__subclasses__()
    valid_services = {
        subclass.service_key: subclass for subclass in subclasses
    }

    @classmethod
    def _check_service(cls, one_service):
        """Check if the service required is valid.

        Parameters
        ----------
        one_service : (subclass) WeatherService
            A service to query. Examples: NOAA, WEATHER_DOT_COM, ACCUWEATHER.

        Raises
        ------
        NotValidWeatherFormException:
            When a service is not in the list of accepted services.
        """
        if one_service not in cls.valid_services:
            logger.exception("Not valid service sent")
            raise NotValidWeatherFormException("Not valid service sent")

    @classmethod
    def average_temp_services(cls, services, lat, lon):
        """Calculate average temp for selected services.

        Parameters
        ----------
        services : list
            List of services. Examples: NOAA, WEATHER_DOT_COM, ACCUWEATHER.

        Raises
        ------
        NotValidWeatherFormException:
            When a service is not in the list of accepted services.

        Returns
        -------
        int
            Average temp calculated taking every selected service.
        """
        temp_sum = 0
        for one_service in services:
            cls._check_service(one_service)
            one_service = cls.valid_services[one_service]
            temp_sum += one_service().request_temp(lat, lon)
        amount_of_services_queried = len(services)
        average_temp = temp_sum // amount_of_services_queried
        return average_temp

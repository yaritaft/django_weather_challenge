import functools
import json
import logging
import requests
from .exceptions import (
    NotValidWeatherFormException,
    ExternalServiceException,
)
from .validators import check_request_external_api

logger = logging.getLogger(__name__)


class WeatherService:
    """Singleton instance that knows how to take the average temp.

    Return average temp with checked services with given latitude
    and longitude.
    """

    def request_temp(self, lat, lon):
        response = self.request_external_api(lat, lon)
        return self._get_fahrenheit(json.loads(response.content))

    @classmethod
    def average_temp_services(cls, services, lat, lon):
        """Calculate average temp for selected services.

        Parameters
        ----------
        services : list
            List of services. Options: NOAA, WEATHER_DOT_COM, ACCUWEATHER.

        Raises
        ------
        NotValidWeatherFormException
            When a service is not in the list of accepted services.

        Returns
        -------
        int
            Average temp calculated taking every selected service.
        """
        temp_sum = 0
        subclasses = cls.__subclasses__()
        dict_services = {
            subclass.service_key: subclass for subclass in subclasses
        }

        for one_service in services:
            if one_service not in map(
                lambda subclass: subclass.service_key, cls.__subclasses__()
            ):
                logger.exception("Not valid service sent")
                raise NotValidWeatherFormException("Not valid service sent")
            one_service = dict_services[one_service]
            temp_sum += one_service().request_temp(lat, lon)
        amount_of_services_queried = len(services)
        average_temp = temp_sum // amount_of_services_queried
        return average_temp


class AccuWeather(WeatherService):
    url = "http://127.0.0.1:5000/accuweather"
    service_key = "ACCUWEATHER"

    def _get_fahrenheit(self, my_dict):
        return int(
            my_dict["simpleforecast"]["forecastday"][0]["current"][
                "fahrenheit"
            ]
        )

    @check_request_external_api(logger)
    def request_external_api(self, lat, lon):
        response = requests.get(
            self.url, params={"latitude": int(lat), "longitude": int(lon)}
        )
        return response


class NoaaWeather(WeatherService):
    url = "http://127.0.0.1:5000/noaa"
    service_key = "NOAA"

    def _get_fahrenheit(self, my_dict):
        return int(my_dict["today"]["current"]["fahrenheit"])

    @check_request_external_api(logger)
    def request_external_api(self, lat, lon):
        lat_long = ",".join((str(lat), str(lon)))
        response = requests.get(self.url, params={"latlon": lat_long})
        return response


class DotComWeather(WeatherService):
    url = "http://127.0.0.1:5000/weatherdotcom"
    service_key = "WEATHER_DOT_COM"

    def _get_fahrenheit(self, my_dict):
        """
        Assumption: It have been assumed that if the unit is not Fahrenheit it
        will be Celsius so the convertion is applied.
        F = (C° * 9/5) + 32
        """
        temp = int(
            my_dict["query"]["results"]["channel"]["condition"]["temp"],
        )
        if (
            my_dict["query"]["results"]["channel"]["units"]["temperature"]
            == "F"
        ):
            return int(temp)
        else:
            return int(temp * (9 / 5)) + 32

    @check_request_external_api(logger)
    def request_external_api(self, lat, lon):
        response = requests.post(
            self.url, json={"lat": float(lat), "lon": float(lon)},
        )
        return response


class AverageWeatherService:
    @classmethod
    def average_temp_services(cls, services, lat, lon):
        """Calculate average temp for selected services.

        Parameters
        ----------
        services : list
            List of services. Options: NOAA, WEATHER_DOT_COM, ACCUWEATHER.

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
        subclasses = WeatherService.__subclasses__()
        dict_services = {
            subclass.service_key: subclass for subclass in subclasses
        }

        for one_service in services:
            if one_service not in dict_services:
                logger.exception("Not valid service sent")
                raise NotValidWeatherFormException("Not valid service sent")
            one_service = dict_services[one_service]
            temp_sum += one_service().request_temp(lat, lon)
        amount_of_services_queried = len(services)
        average_temp = temp_sum // amount_of_services_queried
        return average_temp

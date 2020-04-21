import requests
import json


class AccuWeather:
    url = "http://127.0.0.1:5000/accuweather"

    def _get_fahrenheit(self, my_dict):
        return int(my_dict["simpleforecast"]["forecastday"][0]['current']["fahrenheit"])

    def request_temp(self, lat, lon):
        response = requests.get(self.url, params={"latitude": int(lat), "longitude": int(lon)})
        return self._get_fahrenheit(json.loads(response.content))


class NoaaWeather:
    url = "http://127.0.0.1:5000/noaa"

    def _get_fahrenheit(self, my_dict):
        return int(my_dict["today"]['current']["fahrenheit"])

    def request_temp(self, lat, lon):
        lat_long = ",".join((str(lat), str(lon)))
        response = requests.get(self.url, params={"latlon": lat_long})
        return self._get_fahrenheit(json.loads(response.content))


class DotComWeather:
    levels = ("condition",)
    url = "http://127.0.0.1:5000/weatherdotcom"

    def _get_fahrenheit(self, my_dict):
        """

        Assumption: It have been assumed that if the unit is not Fahrenheit it
        will be Celsius so the convertion is applied.
        F = (C° * 9/5) + 32
        """
        temp = int(my_dict["query"]["results"]["channel"]["condition"]["temp"])
        if my_dict["query"]["results"]["channel"]["units"]["temperature"] == 'F':
            return int(temp)
        else:
            return int(temp * (9 / 5)) + 32

    def request_temp(self, lat, lon):
        response = requests.post(
            self.url,
            json={"lat": float(lat), "lon": float(lon)},
        )
        return self._get_fahrenheit(json.loads(response.content))


class GenericWeather:
    dict_services = {
        "NOAA": NoaaWeather,
        "WEATHER_DOT_COM": DotComWeather,
        "ACCUWEATHER": AccuWeather,
    }
    @classmethod
    def average_temp_services(cls, services, lat, lon):
        temp_sum = 0
        for one_service in services:
            one_service = cls.dict_services[one_service]
            temp_sum += one_service().request_temp(lat, lon)
        amount_of_services_queried = len(services)
        average_temp = temp_sum // amount_of_services_queried
        return average_temp



#
# x = DotComWeather()
# y = AccuWeather()
# z = NoaaWeather()
# print(GenericWeather().average_temp_services(services=(x, y, z), lat=33.3, lon=44.4))

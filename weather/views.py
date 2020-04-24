from django.http import JsonResponse
from django.shortcuts import render
from django.utils.datastructures import MultiValueDictKeyError
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view

from weather.exceptions import (
    ExternalServiceException,
    MissingFieldsException,
    NotValidServicesException,
)
from weather.forms import WeatherAverageForm
from weather.weather_classes import AverageWeatherService


class WeatherIndexView(View):
    """
    Weather view.

    Get: for accessing the form.
    Post: is for receiving data, request external APIs
    and show results or error message.
    """

    def get(self, request):
        """Get the form and render it.

        Parameters
        ----------
        request : HttpRequest
            Request http with method get.

        Returns
        -------
        HttpResponse
            Form html with validations.
        """
        form = {"form": WeatherAverageForm()}
        return render(request, "weather/weather_form.html", form)

    def post(self, request):
        """Show results or error message based in data received.

        Payload:
        It receives services to query, latitude and longitude.
        In order to query every checked service and return an
        average temperature between every service, taking
        current temperature as the value from every service.

        Assumption:
        The average is between services and not between high, low
        and current temperature from each service.

        Parameters
        ----------
        request: HttpRequest
            HTTP Post with latitude, longitude and services to query.

        Raises
        ------
        NotValidWeatherFormException
            If the form sent is not valid.

        Returns
        -------
        HttpResponse
            Results if the post was successful.
            Error message if there was an error.
        """
        try:
            form = WeatherAverageForm(request.POST)
            services = request.POST.getlist("services", default=None)
            lat, lon = request.POST["latitude"], request.POST["longitude"]
            if not (form.is_valid() and form.non_field_errors() == []):
                raise NotValidServicesException("Form sent is not valid")
            average_temp = AverageWeatherService.average_temp_services(
                services, lat, lon
            )
            return render(
                request, "weather/results.html", {"average_temp": average_temp}
            )
        except NotValidServicesException:
            return render(
                request,
                "weather/error_message.html",
                {"message": NotValidServicesException.message},
            )
        except ExternalServiceException:
            return render(
                request,
                "weather/error_message.html",
                {"message": ExternalServiceException.message},
            )
        except MultiValueDictKeyError:
            return render(
                request,
                "weather/error_message.html",
                {"message": MissingFieldsException.message},
            )
        except Exception:
            return render(
                request,
                "weather/error_message.html",
                {"message": "There was an error."},
            )


@api_view(["POST"])
@csrf_exempt
def weather_api(request):
    """Show results or error message based in data received.

    Payload:
    It receives services to query, latitude and longitude.
    In order to query every checked service and return an
    average temperature between every service, taking
    current temperature as the value from every service.

    Assumption:
    The average is between services and not between high, low
    and current temperature from each service.

    Parameters
    ----------
    request: HttpRequest
        HTTP Post with latitude, longitude and services to query.

    Returns
    -------
    HttpResponse
        Results if the post was successful.
        Error message if there was an error.
    """
    try:
        services = request.data.get("services", None)
        lat, lon = (
            request.data.get("latitude", None),
            request.data.get("longitude", None),
        )
        average_temp = AverageWeatherService.average_temp_services(
            services, lat, lon
        )
        return JsonResponse(data={"average_temp": average_temp}, status=200)
    except MissingFieldsException:
        return JsonResponse(
            data={"message": MissingFieldsException.message}, status=400
        )
    except NotValidServicesException:
        return JsonResponse(
            data={"message": NotValidServicesException.message}, status=400
        )
    except ExternalServiceException:
        return JsonResponse(
            data={"message": ExternalServiceException.message}, status=400
        )
    except Exception:
        return JsonResponse(data={"message": "There is an error."}, status=400)

from django.shortcuts import render
from django.views import View
from .forms import WeatherAverageForm
from .weather_classes import AverageWeatherService
from .exceptions import (
    NotValidWeatherFormException,
    ExternalServiceException,
)


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
        form = WeatherAverageForm(request.POST)
        services = request.POST.getlist("services")
        lat, lon = request.POST["latitude"], request.POST["longitude"]
        try:
            if not (form.is_valid() and form.non_field_errors() == []):
                raise NotValidWeatherFormException("Form sent is not valid")
            average_temp = AverageWeatherService.average_temp_services(
                services, lat, lon
            )
            return render(
                request, "weather/results.html", {"average_temp": average_temp}
            )
        except NotValidWeatherFormException:
            return render(
                request,
                "weather/error_message.html",
                {"message": NotValidWeatherFormException.message},
            )
        except ExternalServiceException:
            return render(
                request,
                "weather/error_message.html",
                {"message": ExternalServiceException.message},
            )

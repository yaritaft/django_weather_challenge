from django.shortcuts import render
from django.views import View
from .forms import AxisForm
from .api_services import GenericWeather


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
        form = {"form": AxisForm()}
        return render(request, "weather/index.html", form)

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

        Returns
        -------
        HttpResponse
            Results if the post was successful.
            Error message if there was an error.
        """
        form = AxisForm(request.POST)
        services = request.POST.getlist("services")
        lat, lon = request.POST["latitude"], request.POST["longitude"]
        if form.is_valid() and form.non_field_errors() == []:
            average_temp = GenericWeather.average_temp_services(
                services, lat, lon
            )
            return render(
                request, "weather/results.html", {"average_temp": average_temp}
            )
        return render(request, "weather/error_message.html",)

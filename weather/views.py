from django.shortcuts import render
from django.views import View
from .forms import AxisForm
from .api_services import GenericWeather


class WeatherIndexView(View):
    def get(self, request):
        form = {"form": AxisForm()}
        return render(request, 'weather/index.html', form)

    def post(self, request):
        form = AxisForm(request.POST)
        services = request.POST.getlist("services")
        lat = request.POST['latitude']
        lon = request.POST['longitude']
        print(request.POST.getlist("services"))
        if form.is_valid() and form.non_field_errors() == []:
            average_temp = GenericWeather.average_temp_services(services, lat, lon)
            return render(request, "weather/results.html", {"average_temp": average_temp})
        return render(request, "weather/error_message.html",)

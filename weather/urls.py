from django.urls import path

from weather.views import weather_api, WeatherIndexView

urlpatterns = [
    path("", WeatherIndexView.as_view(), name="main-view"),
    path("json/", weather_api, name="weather"),
]

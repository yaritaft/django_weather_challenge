from django.urls import path

from weather.views import weather_api, WeatherIndexView

urlpatterns = [
    path("", WeatherIndexView.as_view(), name="main-view"),
    path("api/", weather_api, name="weather"),
]

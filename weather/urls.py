from django.urls import path

from weather.views import api_post, WeatherIndexView

urlpatterns = [
    path("", WeatherIndexView.as_view(), name="main-view"),
    path("json/", api_post, name="weather"),
]

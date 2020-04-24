from django.urls import path

from weather.views import WeatherIndexView, api_post

urlpatterns = [
    path("", WeatherIndexView.as_view(), name="main-view"),
    path("json/", api_post, name="weather"),
]

from django.urls import path
from .views import WeatherIndexView

urlpatterns = [
    path('', WeatherIndexView.as_view(), name='main-view'),
]
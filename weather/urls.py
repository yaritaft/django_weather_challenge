from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from weather.views import WeatherApi, WeatherIndexView

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version="v1",
        description="Test description",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("", WeatherIndexView.as_view(), name="main-view"),
    path("api/", csrf_exempt(WeatherApi.as_view()), name="weather"),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
]

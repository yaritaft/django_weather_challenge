import logging

from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from marshmallow.exceptions import ValidationError
from rest_framework.decorators import api_view

from weather.exceptions import ExternalServiceException
from weather.forms import WeatherAverageForm
from weather.schemas import (
    AverageTempFormRequestSchema,
    AverageTempRequestSchema,
)
from weather.weather_classes import AverageWeatherService

logger = logging.getLogger(__name__)


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

        Returns
        -------
        HttpResponse
            Results if the post was successful.
            Error message if there was an error.
        """
        try:
            mutable_query_dict = request.POST.copy()
            serializer = AverageTempFormRequestSchema().load(
                mutable_query_dict
            )
            services, lat, lon = (
                serializer["services"],
                serializer["lat"],
                serializer["lon"],
            )
            average_temp = AverageWeatherService.average_temp_services(
                services, lat, lon
            )
            return render(
                request, "weather/results.html", {"average_temp": average_temp}
            )
        except ValidationError:
            return render(
                request,
                "weather/error_message.html",
                {"message": "Some fields are not right."},
            )
        except ExternalServiceException:
            return render(
                request,
                "weather/error_message.html",
                {"message": ExternalServiceException.message},
            )
        except Exception:
            return render(
                request,
                "weather/error_message.html",
                {"message": "There was an error."},
            )


@swagger_auto_schema(
    method="POST",
    operation_description="Request average temp from services.",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=["latitude", "longitude", "services"],
        properties={
            "latitude": openapi.Schema(
                type=openapi.TYPE_NUMBER,
                format=openapi.FORMAT_FLOAT,
                description="""Value that indicates the latitude.
                Can go from -180 to 180.""",
            ),
            "longitude": openapi.Schema(
                type=openapi.TYPE_NUMBER,
                format=openapi.FORMAT_FLOAT,
                description="""Value that indicates the longitude.
                Can go from -180 to 180.""",
            ),
            "services": openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Items(type=openapi.TYPE_STRING),
                description="""List of services to query.
                Example:
                    ["NOAA", "ACCUWEATHER", "WEATHER_DOT_COM"]
                """,
            ),
        },
    ),
    security=[],
    tags=["weather"],
    responses={
        200: openapi.Response(
            "Average current temp from services queried in Fahrenheint."
        ),
        400: openapi.Response(
            "When services, latitude or longitud are not provided properly."
        ),
    },
)
@api_view(["POST"])
@csrf_exempt
def weather_api(request):  # noqa: D103
    try:
        serializer = AverageTempRequestSchema().loads(request.body)
        services, lat, lon = (
            serializer["services"],
            serializer["lat"],
            serializer["lon"],
        )
        average_temp = AverageWeatherService.average_temp_services(
            services, lat, lon
        )

        return JsonResponse(data={"average_temp": average_temp}, status=200)
    except ExternalServiceException:
        return JsonResponse(
            data={"message": ExternalServiceException.message}, status=400
        )
    except ValidationError:
        return JsonResponse(
            data={"message": "Some fields are not right."}, status=400
        )
    except Exception as e:
        logger.exception("This exception was raised. %s", e)
        return JsonResponse(data={"message": "There is an error."}, status=400)

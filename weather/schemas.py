from marshmallow import EXCLUDE, pre_load
from marshmallow.validate import Length, OneOf, Range
from rest_marshmallow import fields, Schema

from weather.weather_classes import AverageWeatherService


class AverageTempRequestSchema(Schema):
    """Schema for requesting average temp.

    ---
    parameters:
      latitude: float
      longitude: float
      services: ["ACCUWEATHER, WEATHER_DOT_COM, NOAA]
    """

    lat = fields.Float(
        load_only=True,
        validate=Range(min=-180, max=180),
        data_key="latitude",
        required=True,
    )
    lon = fields.Float(
        load_only=True,
        validate=Range(min=-180, max=180),
        data_key="longitude",
        required=True,
    )
    services = fields.List(
        fields.String(
            validate=[OneOf(AverageWeatherService.valid_services)],
            load_only=True,
        ),
        validate=Length(min=1),
        required=True,
    )


class AverageTempFormRequestSchema(Schema):
    """Schema for requesting average temp.

    ---
    parameters:
      latitude: float
      longitude: float
      services: ["ACCUWEATHER, WEATHER_DOT_COM, NOAA]
    """

    class Meta:
        """Schema metaclass."""

        unknown = EXCLUDE

    lat = fields.Float(
        load_only=True,
        validate=Range(min=-180, max=180),
        data_key="latitude",
        required=True,
    )
    lon = fields.Float(
        load_only=True,
        validate=Range(min=-180, max=180),
        data_key="longitude",
        required=True,
    )
    services = fields.List(
        fields.String(
            validate=[OneOf(AverageWeatherService.valid_services)],
            load_only=True,
        ),
        validate=Length(min=1),
        required=True,
    )

    @pre_load
    def cast_latitude_longitude(self, data, **kwargs):
        """Query dict has a particular type of list to extract.

        Parameters
        ----------
        data: QueryDict (mutable)
            request.POST mutable version taken from form.

        Returns
        -------
        QueryDict (mutable)
            Query dict with a standard type of list or None
            value if no list was given.
        """
        data["services"] = data.getlist("services", None)
        return data

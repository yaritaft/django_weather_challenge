class NotValidWeatherFormException(Exception):
    """Exception for not valid form requests."""

    pass


class ExternalServiceException(Exception):
    """Exception for failing external APIs."""

    pass

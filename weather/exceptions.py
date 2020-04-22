class NotValidWeatherFormException(Exception):
    """Exception for not valid form requests."""

    message = "You did not select any service to query."


class ExternalServiceException(Exception):
    """Exception for failing external APIs."""

    message = "There was an error requesting some external API."

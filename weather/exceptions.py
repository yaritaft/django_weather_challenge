class NotValidServicesException(Exception):
    """Exception for not valid form requests."""

    message = "There is a not valid service or no services were provided."


class ExternalServiceException(Exception):
    """Exception for failing external APIs."""

    message = "There was an error requesting some external API."


class MissingFieldsException(Exception):
    """Exception for missing fields."""

    message = "There are missing fields in the request."

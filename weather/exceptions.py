class ExternalServiceException(Exception):
    """Exception for failing external APIs."""

    message = "There was an error requesting some external API."

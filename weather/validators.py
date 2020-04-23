from .exceptions import ExternalServiceException


def check_request_external_api(logger):
    """Wrap the passed in function and log exception.

    @param logger: The logging object
    """

    def check_exceptions(func):
        def wrapper(*args, **kwargs):
            try:
                response = func(*args, **kwargs)
                if response.status_code != 200:
                    logger.exception(
                        "There was an error with these args: %s", *args
                    )
                    raise ExternalServiceException(
                        f"There was an error with these args: {args}"
                    )
                else:
                    return response
            except ExternalServiceException:
                logger.exception("Non 200 Status code in %s", func.__name__)
                raise
            except Exception as e:
                logger.exception(
                    "No API response in %s Exception: %s", func.__name__, e
                )
                raise

        return wrapper

    return check_exceptions

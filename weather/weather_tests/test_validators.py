from django.http import HttpResponse
from django.test import TestCase
import os
from weather.validators import check_request_external_api
from weather.exceptions import ExternalServiceException
import logging
import requests
import mock

logger = logging.getLogger(__name__)


def failingFunc(*args, **kwargs):
    raise TypeError


class TestWeatherValidators(TestCase):
    def setUp(self):
        self.wrapped_request = check_request_external_api(logger)(
            self.client.get
        )
        self.wrapped_failing_func = check_request_external_api(logger)(
            failingFunc
        )

    def test_check_request_external_api_ok(self):
        response = self.wrapped_request("/")
        assert response.status_code == 200

    def test_check_request_external_api_no_response(self):
        self.assertRaises(
            ExternalServiceException, self.wrapped_request, "/wrong_route"
        )

    def test_check_request_external_api_non_200_status_code(self):
        self.assertRaises(TypeError, self.wrapped_failing_func)

# Here we are using the Python implementation of the Illuminate library,
# which is highly inspired by the Laravel framework. This library follows
# similar design patterns and principles as Laravel in PHP.
# For more details, you can check out the GitHub repository:
#
# Github: https://github.com/krunaldodiya/python-laravel
# Author: Krunal Dodiya
# Email: kunal.dodiya1@gmail.com
#
from django.http import HttpRequest
from Illuminate.Exceptions.UnauthorizedAccessException import (
    UnauthorizedAccessException,
)
from Illuminate.Exceptions.RouteNotFoundException import RouteNotFoundException
from Illuminate.Http.Request import Request
from djing.core.Foundation.Djing import Djing
from djing.core.Exceptions.InvalidLicenseException import InvalidLicenseException
from djing.djing_application import djing_application
from djing.djing_request_adapter import DjingRequestAdapter


class DjingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        try:
            application = djing_application()

            request_adapter = DjingRequestAdapter(request)

            djing_request = Request.create_from(application, request_adapter)

            Djing.flush_state("before", djing_request)

            response = application.handle_request(djing_request)

            Djing.flush_state("after", djing_request)

            return response
        except UnauthorizedAccessException:
            print("UnauthorizedAccessException")
            return self.get_response(request)
        except RouteNotFoundException:
            print("RouteNotFoundException")
            return self.get_response(request)
        except InvalidLicenseException:
            print("InvalidLicenseException")
            return self.get_response(request)

from typing import Any, Callable
from Illuminate.Contracts.Foundation.Application import Application
from inertia import share
from Illuminate.Routing.ResponseFactory import ResponseFactory
from djing.core.Http.Requests.DjingRequest import DjingRequest
from djing.core.Facades.Djing import Djing


class HandleInertiaRequests:
    def __init__(self, app: Application) -> None:
        self.__app = app

    def handle(self, request: DjingRequest, next: Callable[[Any], Any]):
        def errors():
            return request.session("errors")

        def user():
            return Djing.user(request)

        def valid_license():
            current_user = Djing.user(request)

            if not current_user:
                return False

            return Djing.check_license_validity()

        def djing_config():
            data = Djing.json_variables(request)

            json_data = ResponseFactory.serialize(data)

            return json_data

        share(
            request=request.request_adapter.request,
            errors=errors,
            current_user=user,
            djing_config=djing_config,
            valid_license=valid_license,
        )

        return next(request)

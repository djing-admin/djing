from typing import Any, Callable
from Illuminate.Contracts.Foundation.Application import Application
from Illuminate.Exceptions.UnauthorizedAccessException import (
    UnauthorizedAccessException,
)
from djing.core.Http.Requests.DjingRequest import DjingRequest
from djing.core.Facades.Djing import Djing


class Authorize:
    def __init__(self, app: Application) -> None:
        self.__app = app

    def handle(self, request: DjingRequest, next: Callable[[Any], Any]):
        if Djing.check(request):
            return next(request)
        else:
            raise UnauthorizedAccessException("Unauthorized: Authorize.handle")

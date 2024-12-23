from typing import Any, Callable
from Illuminate.Contracts.Foundation.Application import Application
from djing.core.Http.Requests.DjingRequest import DjingRequest
from djing.core.Events.ServingDjing import ServingDjing


class DispatchServingDjingEvent:
    def __init__(self, app: Application) -> None:
        self.__app = app

    def handle(self, request: DjingRequest, next: Callable[[Any], Any]):
        ServingDjing.dispatch(request)

        return next(request)

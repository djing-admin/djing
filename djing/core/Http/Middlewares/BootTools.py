from typing import Any, Callable

from Illuminate.Contracts.Foundation.Application import Application
from djing.core.Http.Requests.DjingRequest import DjingRequest
from djing.core.Facades.Djing import Djing


class BootTools:
    def __init__(self, app: Application) -> None:
        self.__app = app

    def handle(self, request: DjingRequest, next: Callable[[Any], Any]):
        Djing.boot_tools(request)

        return next(request)

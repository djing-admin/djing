from typing import Any, Callable
from Illuminate.Contracts.Foundation.Application import Application
from djing.core.Http.Requests.DjingRequest import DjingRequest
from djing.core.Events.DjingServiceProviderRegistered import (
    DjingServiceProviderRegistered,
)
from djing.core.Util import Util


class ServeDjing:
    def __init__(self, app: Application) -> None:
        self.__app = app

    def handle(self, request: DjingRequest, next: Callable[[Any], Any]):
        djing_request = Util.is_djing_request(request)

        if djing_request:
            DjingServiceProviderRegistered.dispatch()

        return next(request)

from typing import Any, Callable
from django.shortcuts import redirect
from Illuminate.Contracts.Foundation.Application import Application
from djing.core.Http.Requests.DjingRequest import DjingRequest
from djing.core.Facades.Djing import Djing


class Authenticate:
    def __init__(self, app: Application) -> None:
        self.__app = app

    def handle(self, request: DjingRequest, next: Callable[[Any], Any]):
        user = Djing.user(request)

        if not user:
            return redirect(Djing.login_path())
        else:
            return next(request)

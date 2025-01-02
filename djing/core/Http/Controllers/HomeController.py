from typing import Any
from django.shortcuts import redirect
from djing.core.Http.Requests.DjingRequest import DjingRequest
from djing.core.Facades.Djing import Djing


class HomeController:
    def home(self, request: DjingRequest) -> Any:
        return redirect(Djing.url(Djing.resolve_initial_path(request)))

from typing import Any, Callable, Optional
from Illuminate.Support.Facades.App import App
from djing.core.Http.Requests.DjingRequest import DjingRequest


class AuthorizesRequests:
    _auth_using_callback: Optional[Callable[[Any], Any]] = None

    @classmethod
    def auth(cls, callback: Callable[[Any], Any]):
        cls._auth_using_callback = callback

        return cls

    @classmethod
    def check(cls, request: DjingRequest) -> bool:
        if cls._auth_using_callback:
            return cls._auth_using_callback(request)

        return App.make("env") == "development"

from typing import Any, List
from inertia import render

from django.shortcuts import redirect
from django.contrib.auth import get_user_model, authenticate, login, logout

from Illuminate.Routing.Controllers.HasMiddleware import HasMiddleware, Middleware
from Illuminate.Support.Facades.Validator import Validator
from djing.core.Http.Requests.DjingRequest import DjingRequest
from djing.core.Facades.Djing import Djing
from djing.core.Rules.Exists import Exists


class LoginController(HasMiddleware):
    def __init__(self) -> None:
        self.djing_path = Djing.url("/")
        self.djing_login_path = Djing.url("/login")

    @classmethod
    def middleware(cls) -> List[str | Middleware]:
        return [Middleware("djing.guest").set_exclude("process_logout")]

    def login(self, request: DjingRequest) -> Any:
        return render(request.request_adapter.request, "Djing.Login")

    def process_login(self, request: DjingRequest) -> Any:
        data = request.json()

        UserModel = get_user_model()

        username_field = data.get("username_field")
        username = data.get("username")
        password = data.get("password")

        rules: dict = {
            "username": ["required", Exists(UserModel, username_field)],
            "password": ["required", "min:8"],
        }

        if username_field == "email":
            rules["username"].insert(0, "email")

        validator = Validator.make(
            data, rules, {"username.email": "Must be a valid email address."}
        )

        response = validator.validate()

        if not response.validated:
            errors = {key: value[0] for key, value in response.errors.items()}

            request.request_adapter.request.session["errors"] = errors

            return redirect(self.djing_login_path)

        credentials = {username_field: username, "password": password}

        user = authenticate(**credentials)

        if user is not None:
            login(request.request_adapter.request, user)

            return redirect(self.djing_path)

        request.request_adapter.request.session["errors"] = {
            "password": "Invalid credentials or User is not activate"
        }

        return redirect(self.djing_login_path)

    def process_logout(self, request: DjingRequest) -> Any:
        logout(request.request_adapter.request)

        return redirect(self.djing_login_path)

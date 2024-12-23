from typing import Self

from django.shortcuts import redirect

from Illuminate.Routing.Router import Router
from Illuminate.Support.Facades.Config import Config
from Illuminate.Support.Facades.Route import Route
from djing.core.Http.Controllers.HomeController import HomeController
from djing.core.Http.Controllers.pages.DashboardController import DashboardController
from djing.core.Http.Controllers.LoginController import LoginController
from djing.core.Facades.Djing import Djing
from djing.core.Http.Controllers.pages.ResourceCreateController import (
    ResourceCreateController,
)
from djing.core.Http.Controllers.pages.ResourceDetailController import (
    ResourceDetailController,
)
from djing.core.Http.Controllers.pages.ResourceIndexController import (
    ResourceIndexController,
)
from djing.core.Http.Controllers.pages.ResourceReplicateController import (
    ResourceReplicateController,
)
from djing.core.Http.Controllers.pages.ResourceUpdateController import (
    ResourceUpdateController,
)
from djing.core.Http.Controllers.pages.LensController import LensController


class PendingRouteRegistration:
    def __init__(self) -> None:
        self.__registered = False

    def with_authentication_routes(self) -> Self:
        Djing.with_authentication()

        attributes = {
            "as": "djing.pages.",
            "prefix": Djing.path(),
            "middleware": ["djing"],
        }

        Route.group(attributes, self.__load_guest_routes)

        return self

    def register(self):
        if not self.__registered:
            self.__register_routes()

    def __register_routes(self):
        attributes = {
            "as": "djing.pages.",
            "prefix": Djing.path(),
            "middleware": Config.get("djing.api_middleware", []),
        }

        Route.group(attributes, self.__load_auth_routes)

        self.__registered = True

    def __load_guest_routes(self, router: Router):
        Route.get("login", [LoginController, "login"]).name("djing.pages.login")
        Route.post("login", [LoginController, "process_login"]).name("djing.login")

    def __load_auth_routes(self, router: Router):
        Route.get("", [HomeController, "home"]).name("home")

        Route.get("dashboard", lambda: redirect(Djing.url())).name("dashboard")

        Route.get("dashboards/:name", DashboardController).name("dashboard.custom")

        Route.get("resources/:resource", ResourceIndexController).name("index")

        Route.get("resources/:resource/new", ResourceCreateController).name("create")

        Route.get("resources/:resource/:resource_id", ResourceDetailController).name(
            "detail"
        )

        Route.get(
            "resources/:resource/:resource_id/edit", ResourceUpdateController
        ).name("edit")

        Route.get(
            "resources/:resource/:resource_id/replicate", ResourceReplicateController
        ).name("replicate")

        Route.get("resources/:resource/lens/:lens", LensController).name("lens")

        Route.post("logout", [LoginController, "process_logout"]).name("djing.logout")

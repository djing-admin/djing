from Illuminate.Contracts.Foundation.Application import Application
from Illuminate.Support.Facades.Gate import Gate
from djing.core.Foundation.Djing import Djing
from djing.core.Providers.DjingApplicationServiceProvider import (
    DjingApplicationServiceProvider,
)
from djing_admin.app.Djing.Dashboards.Main import Main


class DjingServiceProvider(DjingApplicationServiceProvider):
    def __init__(self, app: Application) -> None:
        super().__init__(app)

    def boot(self):
        super().boot()

    def routes(self):
        Djing.routes().with_authentication_routes().register()

    def gate(self):
        def view_djing(user):
            return user and user.email in []

        Gate.define("view_djing", view_djing)

    def dashboards(self):
        return [
            Main.make(),
        ]

    def tools(self):
        return []

    def register(self):
        Djing.with_breadcrumbs()

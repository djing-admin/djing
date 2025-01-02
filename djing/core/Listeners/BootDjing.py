from Illuminate.Contracts.Foundation.Application import Application
from Illuminate.Support.Facades.App import App
from djing.core.Facades.Djing import Djing
from djing.core.Providers.DjingServiceProvider import DjingServiceProvider
from djing.core.Tools.Dashboard import Dashboard
from djing.core.Tools.ResourceManager import ResourceManager


class BootDjing:
    def handle(self, event):
        application: Application = App.make("app")

        if not application.provider_is_loaded(DjingServiceProvider):
            application.register(DjingServiceProvider)

        self.regiter_tools()

    def regiter_tools(self):
        Djing.tools(
            [
                Dashboard(),
                ResourceManager(),
            ]
        )

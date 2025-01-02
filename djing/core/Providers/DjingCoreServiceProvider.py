from Illuminate.Contracts.Foundation.Application import Application
from Illuminate.Contracts.Http.Kernel import Kernel
from Illuminate.Support.Facades.Route import Route
from Illuminate.Support.Facades.Config import Config
from Illuminate.Support.ServiceProvider import ServiceProvider
from Illuminate.Support.Facades.Event import Event
from djing.core.Contracts.QueryBuilder import QueryBuilder
from djing.core.Http.Requests.DjingRequest import DjingRequest
from djing.core.Foundation.Djing import Djing
from djing.core.Http.Middlewares.ServeDjing import ServeDjing
from djing.core.Providers.DjingServiceProvider import DjingServiceProvider
from djing.core.Query.Builder import Builder
from djing.core.Util import Util
from djing.core.Listeners.BootDjing import BootDjing


class DjingCoreServiceProvider(ServiceProvider):
    def __init__(self, app: Application) -> None:
        self.app = app

    def register(self):
        self.app.singleton("djing", Djing)

        def environment_detector():
            return "production" if not Util.is_dev_mode() else "development"

        self.app.detect_environment(environment_detector)

        def bind_query_builder(app, params):
            return Builder(*params)

        self.app.bind(QueryBuilder, bind_query_builder)

    def boot(self):
        try:
            Djing.booted(BootDjing)

            if self.app.running_in_console():
                self.app.register(DjingServiceProvider)

            Route.middleware_group("djing", Config.get("djing.middleware", []))

            Route.middleware_group("djing:api", Config.get("djing.api_middleware", []))

            kernel: Kernel = self.app.make(Kernel)

            kernel.push_middleware(ServeDjing)

            def register_djing_instance(request, app):
                if not app.bound(DjingRequest):
                    app.instance(DjingRequest, request)

            self.app.after_resolving(DjingRequest, register_djing_instance)

            self.__register_events()

            self.__register_resources()

            self.__register_json_variables()
        except Exception as e:
            print("DjingCoreServiceProvider.boot", e)

    def __register_events(self):
        def on_request_handled():
            if self.app.bound(DjingRequest):
                self.app.forget_binding(DjingRequest)

        Event.listen("RequestHandled", on_request_handled)

    def __register_resources(self):
        self.__register_routes()

    def __register_routes(self):
        try:

            def load_routes(router):
                return self.load_routes_from("djing.routes.api")

            Route.group(self.__route_configuration(), load_routes)
        except Exception as e:
            raise e

    def __route_configuration(self):
        return {
            "as": "djing.api.",
            "prefix": "djing-api",
            "middleware": ["djing:api"],
        }

    def __register_json_variables(self):
        Djing.serving(self.__process_serving)

    def __process_serving(self):
        variables = {
            "app_name": Config.get("djing.app_name", "Djing Admin"),
            "currency": Config.get("djing.currency", "USD"),
            "pagination": Config.get("djing.pagination", "links"),
            "version": Djing.version(),
        }

        Djing.provide_to_script(variables=variables)

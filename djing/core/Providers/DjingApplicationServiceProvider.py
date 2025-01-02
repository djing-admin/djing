from Illuminate.Contracts.Debug.ExceptionHandler import ExceptionHandler
from Illuminate.Support.Facades.Gate import Gate
from Illuminate.Contracts.Foundation.Application import Application
from Illuminate.Support.ServiceProvider import ServiceProvider
from djing.core.Exceptions.DjingExceptionHandler import DjingExceptionHandler
from djing.core.Exceptions.InvalidLicenseException import InvalidLicenseException
from djing.core.Facades.Djing import Djing
from djing.core.Http.Requests.DjingRequest import DjingRequest


class DjingApplicationServiceProvider(ServiceProvider):
    def __init__(self, app: Application) -> None:
        self.app = app

    def register(self):
        pass

    def boot(self):
        try:
            self.gate()

            self.routes()

            Djing.serving(self.__process_serving)
        except Exception as e:
            print("DjingApplicationServiceProvider.boot", e)

    def __process_serving(self):
        self.authorization()

        self.register_exception_handler()

        self.resources()

        Djing.dashboards(self.dashboards())

        Djing.tools(self.tools())

    def authorization(self):
        def check_auth(request: DjingRequest):
            if self.app.make("env") == "development":
                return True

            view_djing = Gate.for_user(Djing.user(request)).check("view_djing")

            if not view_djing:
                return False

            valid_license = Djing.check_license_validity()

            if not valid_license:
                raise InvalidLicenseException("Invalid license")

            return True

        Djing.auth(check_auth)

    def register_exception_handler(self):
        self.app.bind(ExceptionHandler, DjingExceptionHandler)

    def resources(self):
        Djing.resources_in(Djing.app_directory())

    def routes(self):
        Djing.routes().with_authentication_routes()

    def gate(self):
        def view_djing(user):
            return user and user.email in []

        Gate.define("view_djing", view_djing)

    def dashboards(self):
        return []

    def tools(self):
        return []

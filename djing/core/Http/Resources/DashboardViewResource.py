from Illuminate.Exceptions.RouteNotFoundException import RouteNotFoundException
from djing.core.Dashboard import Dashboard
from djing.core.Http.Requests.DashboardRequest import DashboardRequest
from djing.core.Facades.Djing import Djing
from djing.core.Http.Resources.Resource import Resource


class DashboardViewResource(Resource):
    def __init__(self, name):
        self.name = name

    def authorized_dashboard_for_request(self, request: DashboardRequest) -> Dashboard:
        dashboard = Djing.dashboard_for_key(self.name, request)

        if not dashboard:
            raise RouteNotFoundException(
                f"The dashboard {self.name} could not be found."
            )

        return dashboard

    def json(self, request: DashboardRequest):
        dashboard = self.authorized_dashboard_for_request(request)

        return {
            "label": dashboard.label(),
            "cards": request.available_cards(self.name),
            "show_refresh_button": dashboard._show_refresh_button,
            "is_help_card": isinstance(dashboard, Dashboard),
        }

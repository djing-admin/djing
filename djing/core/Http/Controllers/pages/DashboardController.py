from typing import Any
from inertia import render
from Illuminate.Exceptions.RouteNotFoundException import RouteNotFoundException
from Illuminate.Exceptions.UnauthorizedAccessException import (
    UnauthorizedAccessException,
)
from Illuminate.Routing.ResponseFactory import ResponseFactory
from djing.core.Facades.Djing import Djing
from djing.core.Http.Requests.DashboardRequest import DashboardRequest
from djing.core.Menu.Breadcrumb import Breadcrumb
from djing.core.Menu.Breadcrumbs import Breadcrumbs
from djing.core.Http.Resources.DashboardViewResource import DashboardViewResource


class DashboardController:
    def __call__(self, request: DashboardRequest) -> Any:
        try:
            name = request.route_param("name")

            dashboard_view_resource = DashboardViewResource.make(name)

            dashboard_view_resource.authorized_dashboard_for_request(request)

            data = {
                "name": name,
                "breadcrumbs": self._breadcrumbs(name, request),
            }

            json_data = ResponseFactory.serialize(data)

            return render(request.request_adapter.request, "Djing.Dashboard", json_data)
        except RouteNotFoundException:
            return render(request.request_adapter.request, "Djing.Error404")
        except UnauthorizedAccessException:
            return render(request.request_adapter.request, "Djing.Error403")

    def _breadcrumbs(self, name, request):
        return Breadcrumbs.make(
            [
                Breadcrumb.make("Dashboards"),
                Breadcrumb.make(Djing.dashboard_for_key(name, request).label()),
            ]
        )

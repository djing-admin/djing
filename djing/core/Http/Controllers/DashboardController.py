from typing import Any

from django.http import JsonResponse
from Illuminate.Routing.ResponseFactory import ResponseFactory
from djing.core.Http.Requests.DashboardRequest import DashboardRequest
from djing.core.Http.Resources.DashboardViewResource import DashboardViewResource


class DashboardController:
    def __call__(self, request: DashboardRequest) -> Any:
        try:
            name = request.route_param("name")

            dashboard_view_resource = DashboardViewResource.make(name)

            data = dashboard_view_resource.json(request)

            return JsonResponse({"data": ResponseFactory.serialize(data)}, status=200)
        except Exception as e:
            return JsonResponse({"data": str(e)}, status=500)

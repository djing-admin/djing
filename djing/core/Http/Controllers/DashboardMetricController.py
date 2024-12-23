from typing import Any
from django.http import JsonResponse
from Illuminate.Routing.ResponseFactory import ResponseFactory
from djing.core.Http.Requests.DashboardMetricRequest import DashboardMetricRequest


class DashboardMetricController:
    def __call__(self, request: DashboardMetricRequest) -> Any:
        try:
            metric = request.metric()

            data = {"value": metric.resolve(request)}

            return JsonResponse({"data": ResponseFactory.serialize(data)}, status=200)
        except Exception as e:
            return JsonResponse({"data": str(e)}, status=500)

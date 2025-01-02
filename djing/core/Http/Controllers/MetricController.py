from typing import Any
from django.http import JsonResponse
from Illuminate.Routing.ResponseFactory import ResponseFactory
from djing.core.Http.Requests.MetricRequest import MetricRequest


class MetricController:
    def show(self, request: MetricRequest) -> Any:
        try:
            metric = request.metric()

            data = {"value": metric.resolve(request)}

            return JsonResponse({"data": ResponseFactory.serialize(data)}, status=200)
        except Exception as e:
            return JsonResponse({"data": str(e)}, status=500)

from typing import Any
from django.http import JsonResponse
from Illuminate.Routing.ResponseFactory import ResponseFactory
from djing.core.Http.Requests.MetricRequest import MetricRequest


class DetailMetricController:
    def __call__(self, request: MetricRequest) -> Any:
        try:
            metric = request.detail_metric()

            data = {"value": metric.resolve(request)}

            return JsonResponse({"data": ResponseFactory.serialize(data)}, status=200)
        except Exception as e:
            return JsonResponse({"data": str(e)}, status=500)

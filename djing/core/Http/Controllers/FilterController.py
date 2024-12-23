from typing import Any
from django.http import JsonResponse
from Illuminate.Routing.ResponseFactory import ResponseFactory
from djing.core.Http.Requests.DjingRequest import DjingRequest


class FilterController:
    def __call__(self, request: DjingRequest) -> Any:
        try:
            new_resource = request.new_resource()

            data = new_resource.available_filters(request)

            return JsonResponse({"data": ResponseFactory.serialize(data)}, status=200)
        except Exception as e:
            return JsonResponse({"data": str(e)}, status=500)

from typing import Any
from django.http import JsonResponse
from Illuminate.Routing.ResponseFactory import ResponseFactory
from djing.core.Http.Requests.DjingRequest import DjingRequest
from djing.core.Lenses.Lens import Lens


class LensFilterController:
    def __call__(self, request: DjingRequest) -> Any:
        try:
            new_resource = request.new_resource()

            available_lenses = new_resource.available_lenses(request)

            lens: Lens = available_lenses.first(
                lambda lens: lens.uri_key() == request.route_param("lens")
            )

            data = lens.available_filters(request)

            return JsonResponse({"data": ResponseFactory.serialize(data)}, status=200)
        except Exception as e:
            return JsonResponse({"data": str(e)}, status=500)

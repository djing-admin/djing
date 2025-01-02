from typing import Any
from django.http import JsonResponse
from Illuminate.Routing.ResponseFactory import ResponseFactory
from djing.core.Http.Requests.LensRequest import LensRequest
from djing.core.Http.Resources.LensViewResource import LensViewResource


class LensController:
    def index(self, request: LensRequest) -> Any:
        try:
            data = {
                "lenses": request.available_lenses(),
            }

            return JsonResponse({"data": ResponseFactory.serialize(data)}, status=200)
        except Exception as e:
            return JsonResponse({"data": str(e)}, status=500)

    def show(self, request: LensRequest) -> Any:
        try:
            lens_view_resource = LensViewResource.make()

            data = lens_view_resource.json(request)

            return JsonResponse({"data": ResponseFactory.serialize(data)}, status=200)
        except Exception as e:
            return JsonResponse({"data": str(e)}, status=500)

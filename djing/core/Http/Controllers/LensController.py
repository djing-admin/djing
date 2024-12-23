from typing import Any
from django.http import JsonResponse
from Illuminate.Routing.ResponseFactory import ResponseFactory
from djing.core.Http.Requests.LensRequest import LensRequest


class LensController:
    def index(self, request: LensRequest) -> Any:
        try:
            data = {
                "lenses": request.available_lenses(),
            }

            return JsonResponse({"data": ResponseFactory.serialize(data)}, status=200)
        except Exception as e:
            return JsonResponse({"data": str(e)}, status=500)

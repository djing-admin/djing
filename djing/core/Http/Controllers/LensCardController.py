from typing import Any

from django.http import JsonResponse

from Illuminate.Routing.ResponseFactory import ResponseFactory
from djing.core.Http.Requests.LensCardRequest import LensCardRequest


class LensCardController:
    def __call__(self, request: LensCardRequest) -> Any:
        try:
            data = {
                "cards": request.available_cards(),
            }

            return JsonResponse({"data": ResponseFactory.serialize(data)}, status=200)
        except Exception as e:
            return JsonResponse({"data": str(e)}, status=500)

from typing import Any

from django.http import JsonResponse

from Illuminate.Routing.ResponseFactory import ResponseFactory
from djing.core.Http.Requests.CardRequest import CardRequest


class CardController:
    def __call__(self, request: CardRequest) -> Any:
        try:
            data = {
                "cards": request.available_cards(),
            }

            return JsonResponse({"data": ResponseFactory.serialize(data)}, status=200)
        except Exception as e:
            return JsonResponse({"data": str(e)}, status=500)

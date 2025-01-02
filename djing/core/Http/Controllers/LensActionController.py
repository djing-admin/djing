from typing import Any
from django.http import JsonResponse
from Illuminate.Routing.ResponseFactory import ResponseFactory
from Illuminate.Validation.ValidationResponse import ValidationResponse
from djing.core.Http.Requests.LensActionRequest import LensActionRequest
from djing.core.Http.Requests.LensRequest import LensRequest


class LensActionController:
    def index(self, request: LensRequest) -> Any:
        try:
            lens = request.lens()

            data: dict = {
                "actions": lens.available_actions_on_index(request),
            }

            return JsonResponse({"data": ResponseFactory.serialize(data)}, status=200)
        except Exception as e:
            return JsonResponse({"data": str(e)}, status=500)

    def store(self, request: LensActionRequest):
        validation_response: ValidationResponse = request.validate_fields()

        if validation_response.errors:
            return JsonResponse({"errors": validation_response.errors}, status=422)

        data = request.action().handle_request(request)

        return JsonResponse({"data": ResponseFactory.serialize(data)}, status=200)

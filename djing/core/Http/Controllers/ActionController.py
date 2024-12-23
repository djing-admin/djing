from typing import Any
from django.http import JsonResponse
from Illuminate.Routing.ResponseFactory import ResponseFactory
from Illuminate.Validation.ValidationResponse import ValidationResponse
from djing.core.Http.Requests.ActionRequest import ActionRequest
from djing.core.Resource import Resource


class ActionController:
    def index(self, request: ActionRequest) -> Any:
        try:
            resources = request.query_param("resources")

            resource_id = (
                resources[0]
                if isinstance(resources, list) and len(resources) == 1
                else None
            )

            resource = request.new_resource_with(
                request.find_model(resource_id) or request.model()
            )

            data: dict = {
                "actions": self._available_actions(request, resource),
            }

            return JsonResponse({"data": ResponseFactory.serialize(data)}, status=200)
        except Exception as e:
            return JsonResponse({"data": str(e)}, status=500)

    def store(self, request: ActionRequest):
        validation_response: ValidationResponse = request.validate_fields()

        if validation_response.errors:
            return JsonResponse({"errors": validation_response.errors}, status=422)

        data = request.action().handle_request(request)

        return JsonResponse({"data": ResponseFactory.serialize(data)}, status=200)

    def _available_actions(self, request: ActionRequest, resource: Resource):
        display = request.query_param("display")

        if display == "index":
            method = "available_actions_on_index"
        elif display == "detail":
            method = "available_actions_on_detail"
        else:
            method = "available_actions"

        return getattr(resource, method)(request)

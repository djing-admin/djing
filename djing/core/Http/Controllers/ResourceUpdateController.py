from typing import Any
from django.db.models import base
from django.http import JsonResponse
from Illuminate.Routing.ResponseFactory import ResponseFactory
from Illuminate.Validation.ValidationResponse import ValidationResponse
from djing.core.Util import Util
from djing.core.Http.Requests.UpdateResourceRequest import UpdateResourceRequest


class ResourceUpdateController:
    def __call__(self, request: UpdateResourceRequest) -> Any:
        try:
            model: base.Model = request.find_model_or_fail()

            resource = request.new_resource_with(model)

            resource.authorize_to_update(request)

            validation_response: ValidationResponse = resource.validate_for_update(
                request, resource
            )

            if validation_response.errors:
                return JsonResponse({"errors": validation_response.errors}, status=422)

            [model, callback] = resource.fill_for_update(request, model)

            model.save()

            data: dict = {
                "id": Util.get_key_name(model),
                "resource": Util.model_to_dict(model),
            }

            return JsonResponse({"data": ResponseFactory.serialize(data)}, status=200)
        except Exception as e:
            return JsonResponse({"data": str(e)}, status=500)

from typing import Any
from django.http import JsonResponse
from Illuminate.Routing.ResponseFactory import ResponseFactory
from Illuminate.Validation.ValidationResponse import ValidationResponse
from djing.core.Util import Util
from djing.core.Http.Requests.CreateResourceRequest import CreateResourceRequest


class ResourceStoreController:
    def __call__(self, request: CreateResourceRequest) -> Any:
        try:
            resource = request.resource()

            resource.authorize_to_create(request)

            validation_response: ValidationResponse = resource.validate_for_creation(
                request
            )

            if validation_response.errors:
                return JsonResponse({"errors": validation_response.errors}, status=422)

            model_class = resource.new_model()

            [model, callback] = resource.fill(request, model_class)

            model.save()

            data: dict = {
                "id": Util.get_key_name(model),
                "resource": Util.model_to_dict(model),
            }

            return JsonResponse({"data": ResponseFactory.serialize(data)}, status=200)
        except Exception as e:
            return JsonResponse({"data": str(e)}, status=500)

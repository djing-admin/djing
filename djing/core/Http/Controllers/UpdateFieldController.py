from typing import Any
from django.http import JsonResponse
from Illuminate.Routing.ResponseFactory import ResponseFactory
from djing.core.Http.Requests.ResourceUpdateOrUpdateAttachedRequest import (
    ResourceUpdateOrUpdateAttachedRequest,
)
from djing.core.Http.Resources.UpdateViewResource import UpdateViewResource


class UpdateFieldController:
    def __call__(self, request: ResourceUpdateOrUpdateAttachedRequest) -> Any:
        try:
            data = UpdateViewResource.make().json(request)

            return JsonResponse({"data": ResponseFactory.serialize(data)}, status=200)
        except Exception as e:
            return JsonResponse({"data": str(e)}, status=500)

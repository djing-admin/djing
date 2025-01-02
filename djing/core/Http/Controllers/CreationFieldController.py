from typing import Any
from django.http import JsonResponse
from Illuminate.Routing.ResponseFactory import ResponseFactory
from djing.core.Http.Requests.ResourceCreateOrAttachRequest import (
    ResourceCreateOrAttachRequest,
)
from djing.core.Http.Resources.CreateViewResource import CreateViewResource
from djing.core.Http.Resources.ReplicateViewResource import ReplicateViewResource


class CreationFieldController:
    def __call__(self, request: ResourceCreateOrAttachRequest) -> Any:
        try:
            from_resource_id = request.query_param("from_resource_id")

            data = {"from_resource_id": from_resource_id}

            if from_resource_id:
                data = ReplicateViewResource.make(from_resource_id).json(request)
            else:
                data = CreateViewResource.make().json(request)

            return JsonResponse({"data": ResponseFactory.serialize(data)}, status=200)
        except Exception as e:
            return JsonResponse({"data": str(e)}, status=500)

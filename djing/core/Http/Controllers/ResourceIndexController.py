from typing import Any

from django.http import JsonResponse
from Illuminate.Routing.ResponseFactory import ResponseFactory
from djing.core.Http.Requests.ResourceIndexRequest import ResourceIndexRequest
from djing.core.Http.Resources.IndexViewResource import IndexViewResource


class ResourceIndexController:
    def __call__(self, request: ResourceIndexRequest) -> Any:
        try:
            index_view_resource = IndexViewResource.make()

            data = index_view_resource.json(request)

            return JsonResponse({"data": ResponseFactory.serialize(data)}, status=200)
        except Exception as e:
            return JsonResponse({"data": str(e)}, status=500)

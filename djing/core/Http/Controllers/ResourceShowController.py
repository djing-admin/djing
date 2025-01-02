from typing import Any

from django.http import JsonResponse
from Illuminate.Routing.ResponseFactory import ResponseFactory
from djing.core.Http.Requests.ResourceDetailRequest import ResourceDetailRequest
from djing.core.Http.Resources.DetailViewResource import DetailViewResource


class ResourceShowController:
    def __call__(self, request: ResourceDetailRequest) -> Any:
        try:
            detail_view_resource = DetailViewResource.make()

            data = detail_view_resource.json(request)

            return JsonResponse({"data": ResponseFactory.serialize(data)}, status=200)
        except Exception as e:
            return JsonResponse({"data": str(e)}, status=500)

from typing import Any

from django.http import JsonResponse

from Illuminate.Collections.Collection import Collection
from Illuminate.Routing.ResponseFactory import ResponseFactory
from djing.core.Http.Requests.DeleteResourceRequest import DeleteResourceRequest


class ResourceDestroyController:
    def __call__(self, request: DeleteResourceRequest) -> Any:
        try:
            data = request.chunks(150, self.__manage_deletable_models)

            return JsonResponse({"data": ResponseFactory.serialize(data)}, status=200)
        except Exception as e:
            return JsonResponse({"data": str(e)}, status=500)

    def __manage_deletable_models(self, models: Collection):
        models.each(lambda model: model.delete())

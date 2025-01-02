from typing import Any
from inertia import render
from Illuminate.Exceptions.RouteNotFoundException import RouteNotFoundException
from Illuminate.Exceptions.UnauthorizedAccessException import (
    UnauthorizedAccessException,
)
from Illuminate.Routing.ResponseFactory import ResponseFactory
from djing.core.Http.Requests.ResourceIndexRequest import ResourceIndexRequest
from djing.core.Menu.Breadcrumb import Breadcrumb
from djing.core.Menu.Breadcrumbs import Breadcrumbs
from djing.core.Http.Resources.IndexViewResource import IndexViewResource


class ResourceIndexController:
    def __call__(self, request: ResourceIndexRequest) -> Any:
        try:
            resource = request.route_param("resource")

            index_view_resource = IndexViewResource.make()

            index_view_resource.authorized_resource_for_request(request)

            data = {
                "resource_name": resource,
                "breadcrumbs": self._breadcrumbs(request),
            }

            return render(
                request.request_adapter.request,
                "Djing.Index",
                ResponseFactory.serialize(data),
            )
        except RouteNotFoundException:
            return render(request.request_adapter.request, "Djing.Error404")
        except UnauthorizedAccessException:
            return render(request.request_adapter.request, "Djing.Error403")

    def _breadcrumbs(self, request: ResourceIndexRequest):
        return Breadcrumbs.make(
            [
                Breadcrumb.make("Resources"),
                Breadcrumb.resource(request.resource()),
            ]
        )

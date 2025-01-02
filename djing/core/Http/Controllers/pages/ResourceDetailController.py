from typing import Any
from inertia import render

from Illuminate.Exceptions.RouteNotFoundException import RouteNotFoundException
from Illuminate.Exceptions.UnauthorizedAccessException import (
    UnauthorizedAccessException,
)
from Illuminate.Routing.ResponseFactory import ResponseFactory
from djing.core.Http.Requests.ResourceDetailRequest import ResourceDetailRequest
from djing.core.Http.Resources.DetailViewResource import DetailViewResource
from djing.core.Menu.Breadcrumb import Breadcrumb
from djing.core.Menu.Breadcrumbs import Breadcrumbs


class ResourceDetailController:
    def __call__(self, request: ResourceDetailRequest) -> Any:
        try:
            resource_id = request.route_param("resource_id")

            resource = request.resource()

            data = {
                "breadcrumbs": self._breadcrumbs(request),
                "resource_id": resource_id,
                "resource_name": resource.uri_key(),
            }

            return render(
                request.request_adapter.request,
                "Djing.Detail",
                ResponseFactory.serialize(data),
            )
        except RouteNotFoundException:
            return render(request.request_adapter.request, "Djing.Error404")
        except UnauthorizedAccessException:
            return render(request.request_adapter.request, "Djing.Error403")

    def _breadcrumbs(self, request: ResourceDetailRequest):
        detail_view_resource = DetailViewResource.make()

        resource = detail_view_resource.authorized_resource_for_request(request)

        label = resource.singular_label()

        title = resource.get_title()

        return Breadcrumbs.make(
            [
                Breadcrumb.make("Resources"),
                Breadcrumb.resource(request.resource()),
                Breadcrumb.make(f"{label} Details: {title}"),
            ]
        )

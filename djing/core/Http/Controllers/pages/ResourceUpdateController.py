from typing import Any
from inertia import render
from Illuminate.Exceptions.RouteNotFoundException import RouteNotFoundException
from Illuminate.Exceptions.UnauthorizedAccessException import (
    UnauthorizedAccessException,
)
from Illuminate.Routing.ResponseFactory import ResponseFactory
from djing.core.Http.Requests.ResourceUpdateOrUpdateAttachedRequest import (
    ResourceUpdateOrUpdateAttachedRequest,
)
from djing.core.Http.Resources.UpdateViewResource import UpdateViewResource
from djing.core.Menu.Breadcrumb import Breadcrumb
from djing.core.Menu.Breadcrumbs import Breadcrumbs


class ResourceUpdateController:
    def __call__(self, request: ResourceUpdateOrUpdateAttachedRequest) -> Any:
        try:
            request.find_model_or_fail()

            resource_id = request.route_param("resource_id")

            resource = request.resource()

            data = {
                "breadcrumbs": self._breadcrumbs(request),
                "resource_id": resource_id,
                "resource_name": resource.uri_key(),
            }

            return render(
                request.request_adapter.request,
                "Djing.Update",
                ResponseFactory.serialize(data),
            )
        except RouteNotFoundException:
            return render(request.request_adapter.request, "Djing.Error404")
        except UnauthorizedAccessException:
            return render(request.request_adapter.request, "Djing.Error403")

    def _breadcrumbs(self, request: ResourceUpdateOrUpdateAttachedRequest):
        resource_class = request.resource()

        resource = UpdateViewResource.make().new_resource_with(request)

        label = resource.singular_label()

        return Breadcrumbs.make(
            [
                Breadcrumb.make("Resources"),
                Breadcrumb.resource(resource_class),
                Breadcrumb.resource(resource),
                Breadcrumb.make(f"Update {label}"),
            ]
        )

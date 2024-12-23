from typing import Any
from inertia import render
from Illuminate.Exceptions.RouteNotFoundException import RouteNotFoundException
from Illuminate.Exceptions.UnauthorizedAccessException import (
    UnauthorizedAccessException,
)
from Illuminate.Routing.ResponseFactory import ResponseFactory
from djing.core.Http.Requests.ResourceCreateOrAttachRequest import (
    ResourceCreateOrAttachRequest,
)
from djing.core.Menu.Breadcrumb import Breadcrumb
from djing.core.Menu.Breadcrumbs import Breadcrumbs


class ResourceReplicateController:
    def __call__(self, request: ResourceCreateOrAttachRequest) -> Any:
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
                "Djing.Replicate",
                ResponseFactory.serialize(data),
            )
        except RouteNotFoundException:
            return render(request.request_adapter.request, "Djing.Error404")
        except UnauthorizedAccessException:
            return render(request.request_adapter.request, "Djing.Error403")

    def _breadcrumbs(self, request: ResourceCreateOrAttachRequest):
        resource_class = request.resource()

        label = resource_class.singular_label()

        return Breadcrumbs.make(
            [
                Breadcrumb.make("Resources"),
                Breadcrumb.resource(resource_class),
                Breadcrumb.resource(request.find_resource_or_fail()),
                Breadcrumb.make(f"Replicate {label}"),
            ]
        )

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


class ResourceCreateController:
    def __call__(self, request: ResourceCreateOrAttachRequest) -> Any:
        try:
            resource = request.resource()

            resource.authorize_to_create(request)

            data = {
                "breadcrumbs": self._breadcrumbs(request),
                "resource_name": resource.uri_key(),
            }

            return render(
                request.request_adapter.request,
                "Djing.Create",
                ResponseFactory.serialize(data),
            )
        except RouteNotFoundException:
            return render(request.request_adapter.request, "Djing.Error404")
        except UnauthorizedAccessException:
            return render(request.request_adapter.request, "Djing.Error403")

    def _breadcrumbs(self, request: ResourceCreateOrAttachRequest):
        resource = request.resource()

        label = resource.singular_label()

        return Breadcrumbs.make(
            [
                Breadcrumb.make("Resources"),
                Breadcrumb.resource(request.resource()),
                Breadcrumb.make(f"Create {label}"),
            ]
        )

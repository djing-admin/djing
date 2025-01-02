from typing import Any
from inertia import render
from Illuminate.Exceptions.RouteNotFoundException import RouteNotFoundException
from Illuminate.Exceptions.UnauthorizedAccessException import (
    UnauthorizedAccessException,
)
from Illuminate.Routing.ResponseFactory import ResponseFactory
from djing.core.Http.Requests.LensRequest import LensRequest
from djing.core.Http.Resources.LensViewResource import LensViewResource
from djing.core.Menu.Breadcrumb import Breadcrumb
from djing.core.Menu.Breadcrumbs import Breadcrumbs


class LensController:
    def __call__(self, request: LensRequest) -> Any:
        try:
            resource = request.route_param("resource")

            lens_view_resource = LensViewResource.make()

            lens = lens_view_resource.authorized_lens_for_request(request)

            data = {
                "resource_name": resource,
                "breadcrumbs": self._breadcrumbs(request),
                "lens": lens.uri_key(),
                "searchable": lens.searchable,
            }

            return render(
                request.request_adapter.request,
                "Djing.Lens",
                ResponseFactory.serialize(data),
            )
        except RouteNotFoundException:
            return render(request.request_adapter.request, "Djing.Error404")
        except UnauthorizedAccessException:
            return render(request.request_adapter.request, "Djing.Error403")

    def _breadcrumbs(self, request: LensRequest):
        return Breadcrumbs.make(
            [
                Breadcrumb.make("Resources"),
                Breadcrumb.resource(request.resource()),
                Breadcrumb.make(request.lens().name()),
            ]
        )

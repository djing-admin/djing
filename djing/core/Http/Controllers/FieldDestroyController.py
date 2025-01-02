from typing import Any

from django.http import JsonResponse
from Illuminate.Exceptions.RouteNotFoundException import RouteNotFoundException
from djing.core.Contracts.Downloadable import Downloadable
from djing.core.Fields.DeleteField import DeleteField
from djing.core.Http.Requests.ResourceDestroyRequest import ResourceDestroyRequest


class FieldDestroyController:
    def __call__(self, request: ResourceDestroyRequest) -> Any:
        try:
            resource = request.find_resource_or_fail()

            resource.authorize_to_update(request)

            field = (
                resource.update_fields(request)
                .where_instance_of(Downloadable)
                .first(lambda field: field.attribute == request.route_param("field"))
            )

            if not field:
                raise RouteNotFoundException("Field not found")

            DeleteField.for_request(request, field, resource.resource)

            return JsonResponse({"data": None}, status=200)
        except Exception as e:
            return JsonResponse({"data": str(e)}, status=500)

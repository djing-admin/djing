from typing import Any

from django.http import JsonResponse
from Illuminate.Routing.ResponseFactory import ResponseFactory
from Illuminate.Exceptions.RouteNotFoundException import RouteNotFoundException
from djing.core.Contracts.RelatableField import RelatableField
from Illuminate.Collections.helpers import collect
from djing.core.Http.Requests.DjingRequest import DjingRequest


class AssociatableController:
    def __call__(self, request: DjingRequest) -> Any:
        try:
            field_attribute = request.route_param("field_attribute")

            field = (
                request.new_resource()
                .available_fields(request)
                .where_instance_of(RelatableField)
                .first(lambda field: field.relationship_name() == field_attribute)
            )

            if not field:
                raise RouteNotFoundException("Field not found")

            data = field.build_associatable_query(request)

            data = (
                collect(data)
                .map_into(field.resource_class)
                .map(
                    lambda resource: field.format_associatable_resource(
                        request, resource
                    )
                )
            )

            return JsonResponse({"data": ResponseFactory.serialize(data)}, status=200)
        except Exception as e:
            return JsonResponse({"data": str(e)}, status=500)

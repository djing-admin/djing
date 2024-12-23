from django.db.models import base
from Illuminate.Exceptions.UnauthorizedAccessException import (
    UnauthorizedAccessException,
)
from djing.core.Http.Requests.ResourceUpdateOrUpdateAttachedRequest import (
    ResourceUpdateOrUpdateAttachedRequest,
)
from djing.core.Http.Resources.Resource import Resource


class UpdateViewResource(Resource):
    def new_resource_with(self, request: ResourceUpdateOrUpdateAttachedRequest):
        model: base.Model = request.find_model_or_fail()

        resource = request.new_resource_with(model)

        if not resource.authorized_to_update(request):
            raise UnauthorizedAccessException(
                "Unauthorized: UpdateViewResource.new_resource_with"
            )

        return resource

    def json(self, request: ResourceUpdateOrUpdateAttachedRequest):
        resource = self.new_resource_with(request)

        fields = resource.update_fields_within_panels(request, resource)

        panels = resource.available_panels_for_update(request, resource, fields)

        return {
            "title": resource.get_title(),
            "fields": fields,
            "panels": panels,
        }

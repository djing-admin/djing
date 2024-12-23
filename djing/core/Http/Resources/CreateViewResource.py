from djing.core.Http.Requests.ResourceCreateOrAttachRequest import (
    ResourceCreateOrAttachRequest,
)
from djing.core.Http.Resources.Resource import Resource


class CreateViewResource(Resource):
    def json(self, request: ResourceCreateOrAttachRequest):
        resource = self.new_resource_with(request)

        fields = resource.creation_fields_within_panels(request)

        return {
            "fields": fields,
            "panels": resource.available_panels_for_create(request, fields),
        }

    def new_resource_with(self, request: ResourceCreateOrAttachRequest):
        resource_class = request.resource()

        resource_class.authorize_to_create(request)

        return request.new_resource()

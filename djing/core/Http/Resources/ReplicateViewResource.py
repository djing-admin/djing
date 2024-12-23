from django.db.models import base
from djing.core.Http.Requests.ResourceCreateOrAttachRequest import (
    ResourceCreateOrAttachRequest,
)
from djing.core.Http.Resources.CreateViewResource import CreateViewResource


class ReplicateViewResource(CreateViewResource):
    def __init__(self, from_resource_id):
        self.from_resource_id = from_resource_id

    def new_resource_with(self, request: ResourceCreateOrAttachRequest):
        model: base.Model = request.find_model_or_fail(self.from_resource_id)

        resource = request.new_resource_with(model)

        resource.authorize_to_replicate(request)

        return resource

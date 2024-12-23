from django.db.models import base
from Illuminate.Collections.helpers import collect
from Illuminate.Exceptions.UnauthorizedAccessException import (
    UnauthorizedAccessException,
)
from Illuminate.Support.helpers import with_
from djing.core.Fields.FieldCollection import FieldCollection
from djing.core.Http.Requests.ResourceDetailRequest import ResourceDetailRequest
from djing.core.Http.Resources.Resource import Resource


class DetailViewResource(Resource):
    def authorized_resource_for_request(self, request: ResourceDetailRequest):
        model: base.Model = request.find_model_or_fail()

        resource = request.new_resource_with(model)

        if not resource.authorized_to_view(request):
            raise UnauthorizedAccessException(
                "Unauthorized: DetailViewResource.authorized_resource_for_request"
            )

        return resource

    def json(self, request: ResourceDetailRequest):
        resource = self.authorized_resource_for_request(request)

        def map_detail(detail):
            detail["fields"] = collect(detail["fields"]).values().all()

            return detail

        payload = with_(resource.serialize_for_detail(request, resource), map_detail)

        return {
            "title": resource.get_title(),
            "panels": resource.available_panels_for_detail(
                request, resource, FieldCollection.make(payload["fields"])
            ),
            "resource": payload,
        }

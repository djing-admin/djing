from Illuminate.Exceptions.UnauthorizedAccessException import (
    UnauthorizedAccessException,
)
from djing.core.Http.Requests.ResourceIndexRequest import ResourceIndexRequest
from djing.core.Http.Resources.Resource import Resource


class IndexViewResource(Resource):
    def authorized_resource_for_request(self, request: ResourceIndexRequest):
        resource = request.resource()

        if not resource.authorized_to_view_any(request):
            raise UnauthorizedAccessException(
                "Unauthorized: IndexViewResource.authorized_resource_for_request"
            )

        return resource

    def json(self, request: ResourceIndexRequest):
        resource = self.authorized_resource_for_request(request)

        paginator, total, sortable = request.search_index()

        resources = (
            paginator.get_collection()
            .map_into(resource)
            .map(lambda resource: resource.serialize_for_index(request))
        )

        return {
            "label": resource.label(),
            "per_page_options": resource.per_page_options(),
            "resources": resources,
            "total": total,
            "sortable": sortable,
            "per_page": paginator.per_page(),
            "start_record": paginator.start_record(),
            "end_record": paginator.end_record(),
            "num_pages": paginator.num_pages(),
        }

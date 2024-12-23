from Illuminate.Foundation.Http.FormRequest import FormRequest
from djing.core.Http.Requests.InteractsWithResources import InteractsWithResources
from djing.core.Http.Requests.InteractsWithResourcesSelection import (
    InteractsWithResourcesSelection,
)


class DjingRequest(
    FormRequest,
    InteractsWithResources,
    InteractsWithResourcesSelection,
):
    def is_resource_index_request(self):
        return self.request_is("ResourceIndexRequest")

    def is_resource_detail_request(self):
        return self.request_is("ResourceDetailRequest")

    def is_action_request(self):
        return self.segment(3) == "actions"

    def is_create_or_attach_request(self) -> bool:
        return self.request_is("ResourceDetailRequest") or (
            self.query_param("editing")
            and self.query_param("edit_mode") in ["create", "attach"]
        )

    def is_update_or_update_attached_request(self) -> bool:
        return self.request_is("ResourceDetailRequest") or (
            self.query_param("editing")
            and self.query_param("edit_mode") in ["update", "update-attached"]
        )

    def request_is(self, name: str):
        return hasattr(self, "request_name") and getattr(self, "request_name") == name

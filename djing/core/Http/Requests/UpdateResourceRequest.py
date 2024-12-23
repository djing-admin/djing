from djing.core.Http.Requests.DjingRequest import DjingRequest
from djing.core.Http.Requests.QueriesResources import QueriesResources


class UpdateResourceRequest(DjingRequest, QueriesResources):
    request_name = "UpdateResourceRequest"

    def is_update_or_update_attached_request(self) -> bool:
        return True

from djing.core.Http.Requests.DjingRequest import DjingRequest
from djing.core.Http.Requests.QueriesResources import QueriesResources


class ResourceDetailRequest(DjingRequest, QueriesResources):
    request_name = "ResourceDetailRequest"

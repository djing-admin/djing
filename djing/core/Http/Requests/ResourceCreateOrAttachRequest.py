from djing.core.Http.Requests.DjingRequest import DjingRequest
from djing.core.Http.Requests.QueriesResources import QueriesResources


class ResourceCreateOrAttachRequest(DjingRequest, QueriesResources):
    request_name = "ResourceCreateOrAttachRequest"

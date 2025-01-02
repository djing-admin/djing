from djing.core.Http.Requests.DjingRequest import DjingRequest


class CreateResourceRequest(DjingRequest):
    request_name = "CreateResourceRequest"

    def is_create_or_attach_request(self) -> bool:
        return True

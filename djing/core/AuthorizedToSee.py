from djing.core.Http.Requests.DjingRequest import DjingRequest


class AuthorizedToSee:
    see_callback = None

    def authorized_to_see(self, request: DjingRequest):
        if self.see_callback:
            return self.see_callback(request)

        return True

    def can_see(self, callback):
        self.see_callback = callback

        return self

from abc import ABC, abstractmethod
from djing.core.AuthorizedToSee import AuthorizedToSee
from djing.core.Http.Requests.DjingRequest import DjingRequest
from djing.core.Makeable import Makeable


class Tool(ABC, AuthorizedToSee, Makeable):
    def authorize(self, request: DjingRequest):
        return self.authorized_to_see(request)

    def boot(self):
        pass

    @abstractmethod
    def menu(self, request: DjingRequest):
        pass

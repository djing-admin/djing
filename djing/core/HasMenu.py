from abc import abstractmethod
from djing.core.Http.Requests.DjingRequest import DjingRequest


class HasMenu:
    @abstractmethod
    def menu(self, request: DjingRequest):
        pass

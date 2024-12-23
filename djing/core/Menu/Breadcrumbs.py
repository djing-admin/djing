from Illuminate.Contracts.Support.JsonSerializable import JsonSerializable
from Illuminate.Support.Facades.App import App
from djing.core.AuthorizedToSee import AuthorizedToSee
from djing.core.Http.Requests.DjingRequest import DjingRequest
from djing.core.Makeable import Makeable


class Breadcrumbs(AuthorizedToSee, Makeable, JsonSerializable):
    def __init__(self, items=[]):
        self._items = items

    def items(self, items):
        self._items = items

    def json_serialize(self) -> list:
        return self._items if self.authorized_to_see(App.make(DjingRequest)) else []

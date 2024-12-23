from Illuminate.Contracts.Support.JsonSerializable import JsonSerializable
from Illuminate.Support.Facades.App import App
from djing.core.AuthorizedToSee import AuthorizedToSee
from djing.core.Fields.Collapsable import Collapsable
from djing.core.Http.Requests.DjingRequest import DjingRequest
from djing.core.Makeable import Makeable
from djing.core.Menu.MenuCollection import MenuCollection


class MenuGroup(AuthorizedToSee, Makeable, Collapsable, JsonSerializable):
    component = "menu-group"

    def __init__(self, name, items=[]):
        self.name = name

        self._items = MenuCollection(items)

    def json_serialize(self) -> dict:
        request = App.make(DjingRequest)

        return {
            "component": self.component,
            "name": self.name,
            "items": self._items.authorize(request).without_empty_items().all(),
            "collapsable": self._collapsable,
        }

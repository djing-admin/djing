from typing import Self
from Illuminate.Contracts.Support.JsonSerializable import JsonSerializable
from Illuminate.Support.Facades.App import App
from djing.core.AuthorizedToSee import AuthorizedToSee
from djing.core.Fields.Collapsable import Collapsable
from djing.core.Http.Requests.DjingRequest import DjingRequest
from djing.core.Makeable import Makeable
from djing.core.Menu.MenuCollection import MenuCollection


class MenuList(AuthorizedToSee, Makeable, Collapsable, JsonSerializable):
    component = "menu-list"

    def __init__(self, items):
        self.items(items)

    def items(self, items=[]) -> Self:
        self._items = MenuCollection(items)

        return self

    def json_serialize(self) -> dict:
        request = App.make(DjingRequest)

        return {
            "component": self.component,
            "items": self._items.authorize(request).without_empty_items().all(),
        }

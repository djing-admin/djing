from Illuminate.Collections.helpers import collect
from Illuminate.Contracts.Support.JsonSerializable import JsonSerializable
from Illuminate.Database.Serializable import Serializable
from Illuminate.Support.Facades.App import App
from djing.core.Http.Requests.DjingRequest import DjingRequest
from djing.core.Makeable import Makeable


class Menu(Serializable, Makeable, JsonSerializable):
    def __init__(self, items=[]):
        self.items = collect(items)

    @classmethod
    def wrap(cls, menu):
        if isinstance(menu, cls):
            return menu

        return cls.make(menu)

    def json_serialize(self) -> dict:
        request = App.make(DjingRequest)

        items = (
            self.items.flatten()
            .reject(
                lambda item: hasattr(item, "authorized_to_see")
                and not self.check_authorization(request, item)
            )
            .values()
            .json_serialize()
        )

        return items

    def check_authorization(self, request: DjingRequest, item) -> bool:
        if hasattr(item, "authorized_to_see"):
            authorizer = getattr(item, "authorized_to_see")

            return authorizer(request)

        return True

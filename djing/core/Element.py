from abc import ABC
from Illuminate.Contracts.Support.JsonSerializable import JsonSerializable
from djing.core.AuthorizedToSee import AuthorizedToSee
from djing.core.Http.Requests.DjingRequest import DjingRequest
from djing.core.Makeable import Makeable
from djing.core.Metable import Metable


class Element(ABC, AuthorizedToSee, Makeable, Metable, JsonSerializable):
    component = None
    _only_on_detail = False

    def __init__(self, component=None) -> None:
        self.component = component if component else self.component

    def authorize(self, request: DjingRequest):
        return self.authorized_to_see(request)

    def get_component(self):
        return self.component

    def only_on_detail(self):
        self._only_on_detail = True

        return self

    def json_serialize(self) -> dict:
        meta = self.meta()

        current = {
            "component": self.get_component(),
            "prefix_component": False,
            "only_on_detail": self._only_on_detail,
        }

        return {**current, **meta}

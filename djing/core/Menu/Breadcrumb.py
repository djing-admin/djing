from typing import Type
from Illuminate.Contracts.Support.JsonSerializable import JsonSerializable
from Illuminate.Support.Facades.App import App
from djing.core.AuthorizedToSee import AuthorizedToSee
from djing.core.Http.Requests.DjingRequest import DjingRequest
from djing.core.Makeable import Makeable
from djing.core.Resource import Resource


class Breadcrumb(AuthorizedToSee, Makeable, JsonSerializable):
    def __init__(self, name, path=None):
        self._name = name
        self._path = path

    def path(self, path):
        self._path = path

        return self

    @classmethod
    def resource(cls, resource_class: Type[Resource]):
        if isinstance(resource_class, Resource) and resource_class.resource.id:
            label = resource_class.singular_label()
            title = resource_class.get_title()
            uri_key = resource_class.uri_key()
            key = resource_class.get_key()

            return (
                Breadcrumb.make(f"{label} Details: {title}")
                .path(f"/resources/{uri_key}/{key}")
                .can_see(lambda request: resource_class.authorized_to_view(request))
            )

        return (
            Breadcrumb.make(resource_class.label())
            .path(f"/resources/{resource_class.uri_key()}")
            .can_see(
                lambda request: resource_class.available_for_navigation(request)
                and resource_class.authorized_to_view_any(request)
            )
        )

    def json_serialize(self) -> dict:
        return {
            "name": self._name,
            "path": (
                self._path if self.authorized_to_see(App.make(DjingRequest)) else None
            ),
        }

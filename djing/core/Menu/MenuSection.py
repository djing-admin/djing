from typing import TYPE_CHECKING, Type
from Illuminate.Contracts.Support.JsonSerializable import JsonSerializable
from Illuminate.Support.Facades.App import App
from djing.core.AuthorizedToSee import AuthorizedToSee
from djing.core.Fields.Collapsable import Collapsable
from djing.core.Http.Requests.DjingRequest import DjingRequest
from djing.core.Makeable import Makeable
from djing.core.Menu.MenuCollection import MenuCollection
from djing.core.URL import URL
from djing.core.WithIcon import WithIcon

if TYPE_CHECKING:
    from djing.core.Dashboard import Dashboard
    from djing.core.Resource import Resource


class MenuSection(AuthorizedToSee, Makeable, Collapsable, WithIcon, JsonSerializable):
    component = "menu-section"

    def __init__(self, name, items=[], icon="collection"):
        self.name = name
        self.items = MenuCollection(items)
        self._path = None

        self.with_icon(icon)

    def path(self, path=None):
        self._path = path

        return self

    @classmethod
    def dashboard(cls, dashboard_class: Type["Dashboard"]):
        dashboard = dashboard_class()

        return (
            cls.make(dashboard.label())
            .path("/dashboards/" + dashboard.uri_key())
            .can_see(lambda request: dashboard.can_see(request))
        )

    @classmethod
    def resource(cls, resource_class: Type["Resource"]):
        resource = resource_class()

        return (
            cls.make(resource.label())
            .path("/resources/" + resource.uri_key())
            .can_see(
                lambda request: resource_class.available_for_navigation(request)
                and resource_class.authorized_to_view_any(request)
            )
        )

    def json_serialize(self) -> dict:
        request = App.make(DjingRequest)

        url = URL.make(self._path) if self._path else None

        active = url.active() if url else False

        return {
            "component": self.component,
            "name": self.name,
            "items": self.items.authorize(request).without_empty_items(),
            "icon": self._icon,
            "path": self._path,
            "collapsable": self._collapsable,
            "active": active,
        }

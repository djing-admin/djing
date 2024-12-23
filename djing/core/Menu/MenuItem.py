from typing import TYPE_CHECKING, Any, Callable, Type
from Illuminate.Contracts.Support.JsonSerializable import JsonSerializable
from Illuminate.Support.Facades.App import App
from djing.core.AuthorizedToSee import AuthorizedToSee
from djing.core.Facades.Djing import Djing
from djing.core.Http.Requests.DjingRequest import DjingRequest
from djing.core.Makeable import Makeable
from djing.core.URL import URL
from djing.core.WithBadge import WithBadge

if TYPE_CHECKING:
    from djing.core.Dashboard import Dashboard
    from djing.core.Resource import Resource


class MenuItem(AuthorizedToSee, Makeable, WithBadge, JsonSerializable):
    component = "menu-item"

    def __init__(self, name, path=None) -> None:
        self._name = name
        self._path = path
        self._external = False
        self._active_menu_callback: Callable[..., Any] | None = None

        self._badge = None
        self._badge_type = "info"

    def path(self, path=None):
        self._path = path

        return self

    def external(self):
        self._external = True

        return self

    @classmethod
    def external_link(cls, name, path):
        return cls(name, path).external()

    def active_when(self, callback: Callable[..., Any]):
        self._active_menu_callback = callback

        return self

    @classmethod
    def dashboard(cls, dashboard_class: Type["Dashboard"]):
        dashboard = dashboard_class()

        def check_active_url(request, path):
            return request.get_url() == Djing.url(path)

        return (
            cls.make(dashboard.label())
            .path("/dashboards/" + dashboard.uri_key())
            .active_when(check_active_url)
            .can_see(lambda request: dashboard.can_see(request))
        )

    @classmethod
    def resource(cls, resource_class: Type["Resource"]):
        resource = resource_class()

        def check_active_url(request, url: URL):
            return url.active()

        return (
            cls.make(resource.label())
            .path("/resources/" + resource.uri_key())
            .active_when(check_active_url)
            .can_see(
                lambda request: resource_class.available_for_navigation(request)
                and resource_class.authorized_to_view_any(request)
            )
        )

    def _default_active_menu_callback(self, request: DjingRequest, url: URL) -> Any:
        return url.active()

    def json_serialize(self) -> dict:
        url = URL.make(self._path, self._external)

        active_menu_callback: Any = (
            self._active_menu_callback
            if self._active_menu_callback
            else self._default_active_menu_callback
        )

        return {
            "component": self.component,
            "name": self._name,
            "path": self._path,
            "external": self._external,
            "active": active_menu_callback(App.make("request"), url),
            "badge": (
                {
                    "title": self._badge,
                    "type": self._badge_type,
                }
                if self._badge
                else None
            ),
        }

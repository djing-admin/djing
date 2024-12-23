from typing import Any
from Illuminate.Collections.helpers import collect
from Illuminate.Contracts.Support.JsonSerializable import JsonSerializable
from Illuminate.Support.Facades.App import App
from Illuminate.Support.builtins import array_merge
from djing.core.AuthorizedToSee import AuthorizedToSee
from djing.core.Facades.Djing import Djing
from djing.core.Http.Requests.DjingRequest import DjingRequest
from djing.core.Makeable import Makeable
from djing.core.Metable import Metable


class Filter(AuthorizedToSee, Makeable, Metable, JsonSerializable):
    _name = None

    component = "select-filter"

    def name(self):
        return self._name if self._name else Djing.humanize(self)

    def key(self):
        return f"{self.__module__}.{self.__class__.__name__}"

    def default(self):
        return ""

    def options(self, request: DjingRequest):
        return []

    def get_component(self):
        return self.component

    def json_serialize(self) -> dict:
        def map_options(value: Any, label: Any):
            if isinstance(value, dict):
                return array_merge({"label": label}, value)
            elif isinstance(value, str):
                return {"label": label, "value": value}
            else:
                return {"label": value, "value": value}

        data = array_merge(
            {
                "class": self.key(),
                "name": self.name(),
                "component": self.get_component(),
                "options": (
                    collect(self.options(App.make(DjingRequest)))
                    .map(map_options)
                    .values()
                    .all()
                ),
                "current_value": self.default() if self.default() else "",
                "default_value": self.default() if self.default() else "",
            },
            self.meta(),
        )

        return dict(data)

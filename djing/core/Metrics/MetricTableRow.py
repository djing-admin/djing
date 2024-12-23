from typing import Any, Callable, Self
from Illuminate.Contracts.Support.JsonSerializable import JsonSerializable
from djing.core.Makeable import Makeable


class MetricTableRow(Makeable, JsonSerializable):
    _icon = ""
    _icon_class = ""
    _title = ""
    _subtitle = ""
    _action_callback = None

    def __init__(self):
        def default_action_callback():
            return []

        self._action_callback = default_action_callback

    def icon(self, icon: str) -> Self:
        self._icon = icon

        return self

    def icon_class(self, icon_class: str) -> Self:
        self._icon_class = icon_class

        return self

    def title(self, title: str) -> Self:
        self._title = title

        return self

    def subtitle(self, subtitle: str) -> Self:
        self._subtitle = subtitle

        return self

    def actions(self, callback: Callable[..., Any]) -> Self:
        self._action_callback = callback

        return self

    def json_serialize(self):
        return {
            "icon": self._icon,
            "icon_class": self._icon_class,
            "title": self._title,
            "subtitle": self._subtitle,
            "actions": self._action_callback(),
        }

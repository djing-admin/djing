from typing import TYPE_CHECKING, Self
from Illuminate.Helpers.Util import Util
from Illuminate.Support.builtins import array_merge
from djing.core.Element import Element
from djing.core.Http.Requests.DjingRequest import DjingRequest

if TYPE_CHECKING:
    from djing.core.Resource import Resource


class FieldElement(Element):
    _show_on_index = True
    _show_on_detail = True
    _show_on_creation = True
    _show_on_update = True

    panel = None
    assigned_panel = None

    def hide_from_index(self, callback=True) -> Self:
        if callable(callback):
            self._show_on_index = not callback()
        else:
            self._show_on_index = not callback

        return self

    def hide_from_detail(self, callback=True) -> Self:
        if callable(callback):
            self._show_on_detail = not callback()
        else:
            self._show_on_detail = not callback

        return self

    def hide_when_creating(self, callback=True) -> Self:
        if callable(callback):
            self._show_on_creation = not callback()
        else:
            self._show_on_creation = not callback

        return self

    def hide_when_updating(self, callback=True) -> Self:
        if callable(callback):
            self._show_on_update = not callback()
        else:
            self._show_on_update = not callback

        return self

    def show_on_index(self, callback=True) -> Self:
        self._show_on_index = callback

        return self

    def show_on_detail(self, callback=True) -> Self:
        self._show_on_detail = callback

        return self

    def show_on_creating(self, callback=True) -> Self:
        self._show_on_creation = callback

        return self

    def show_on_updating(self, callback=True) -> Self:
        self._show_on_update = callback

        return self

    def is_shown_on_update(self, request: DjingRequest, resource: "Resource"):
        if callable(self._show_on_update):
            self._show_on_update = Util.callback_with_dynamic_args(
                self._show_on_update, [request, resource]
            )

        return self._show_on_update

    def is_shown_on_index(self, request: DjingRequest, resource: "Resource"):
        if callable(self._show_on_index):
            self._show_on_index = Util.callback_with_dynamic_args(
                self._show_on_index, [request, resource]
            )

        return self._show_on_index

    def is_shown_on_detail(self, request: DjingRequest, resource: "Resource"):
        if callable(self._show_on_detail):
            self._show_on_detail = Util.callback_with_dynamic_args(
                self._show_on_detail, [request, resource]
            )

        return self._show_on_detail

    def is_shown_on_creation(self, request: DjingRequest):
        if callable(self._show_on_creation):
            self._show_on_creation = Util.callback_with_dynamic_args(
                self._show_on_creation, [request]
            )

        return self._show_on_creation

    def only_on_index(self):
        self._show_on_index = True
        self._show_on_detail = False
        self._show_on_creation = False
        self._show_on_update = False

        return self

    def only_on_detail(self):
        super().only_on_detail()

        self._show_on_index = False
        self._show_on_detail = True
        self._show_on_creation = False
        self._show_on_update = False

        return self

    def only_on_forms(self):
        self._show_on_index = False
        self._show_on_detail = False
        self._show_on_creation = True
        self._show_on_update = True

        return self

    def except_on_forms(self):
        self._show_on_index = True
        self._show_on_detail = True
        self._show_on_creation = False
        self._show_on_update = False

        return self

    def json_serialize(self):
        return array_merge(
            super().json_serialize(),
            {
                "panel": self.panel,
            },
        )

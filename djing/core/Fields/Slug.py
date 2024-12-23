from typing import Self
from Illuminate.Support.builtins import array_merge
from Illuminate.Support.Str import Str
from Illuminate.Support.Facades.App import App
from djing.core.Contracts.Previewable import Previewable
from djing.core.Fields.Field import Field
from djing.core.Http.Requests.DjingRequest import DjingRequest


class Slug(Field, Previewable):
    component = "slug-field"

    _slug_from: str | None = None
    _separator = "-"
    _show_customize_button = False

    def __init__(self, name, attribute=None, resolve_callback=None):
        super().__init__(name, attribute, resolve_callback)

    def slug_from(self, slug_from: str) -> Self:
        self._slug_from = slug_from

        return self

    def separator(self, separator: str) -> Self:
        self._separator = separator

        return self

    def preview_for(self, value: str) -> str:
        return Str.slug(value, self._separator)

    def json_serialize(self):
        request: DjingRequest = App.make(DjingRequest)

        updating = request.is_update_or_update_attached_request()

        if updating:
            self.readonly()
            self._show_customize_button = True

        return array_merge(
            {
                "updating": updating,
                "slug_from": (
                    self._slug_from.attribute
                    if isinstance(self._slug_from, Field)
                    else Str.lower(self._slug_from).replace(" ", "-")
                ),
                "separator": self._separator,
                "show_customize_button": self._show_customize_button,
            },
            super().json_serialize(),
        )

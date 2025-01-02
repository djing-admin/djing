from typing import Self
from Illuminate.Collections.Arr import Arr
from Illuminate.Collections.helpers import collect
from Illuminate.Support.Facades.App import App
from Illuminate.Support.builtins import array_merge
from Illuminate.Support.helpers import transform
from djing.core.Contracts.FilterableField import FilterableField
from djing.core.Fields.Field import Field
from djing.core.Fields.FieldFilterable import FieldFilterable
from djing.core.Fields.Filters.SelectFilter import SelectFilter
from djing.core.Fields.Searchable import Searchable
from djing.core.Http.Requests.DjingRequest import DjingRequest


class Select(Field, FieldFilterable, FilterableField, Searchable):
    component = "select-field"
    option_callback = None

    def options(self, options) -> Self:
        self.option_callback = options

        return self

    def display_using_labels(self) -> Self:
        def display_callback(value):
            if not value:
                return value

            item = collect(self.serialize_options(False)).first(
                lambda option: option.get("value") == value
            )

            return item["label"] if item else value

        self.display_using(display_callback)

        return self

    def serialize_options(self, searchable: bool = False):
        options = (
            self.option_callback()
            if callable(self.option_callback)
            else self.option_callback
        )

        options = options if isinstance(options, (list, dict)) else {}

        def map_options(label, value):
            if searchable and "group" in label:
                return {
                    "label": label["group"] + " - " + label["label"],
                    "value": value,
                }

            if isinstance(label, dict):
                return {**label, "value": value}

            return {"label": label, "value": value}

        return collect(options).map(map_options).values().all()

    def make_filter(self, request: DjingRequest):
        return SelectFilter(self)

    def serialize_for_filter(self):
        return transform(
            self.json_serialize(),
            lambda field: Arr.only(
                field,
                ["unique_key", "name", "attribute", "options", "type", "searchable"],
            ),
        )

    def json_serialize(self):
        searchable = self.is_searchable(App.make(DjingRequest))

        self.with_meta({"options": self.serialize_options(searchable)})

        return array_merge(
            super().json_serialize(),
            {
                "searchable": self._searchable,
            },
        )

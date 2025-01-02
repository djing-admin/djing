from typing import Self
from Illuminate.Collections.Arr import Arr
from Illuminate.Collections.helpers import collect
from Illuminate.Support.builtins import array_merge
from Illuminate.Support.helpers import transform
from djing.core.Contracts.FilterableField import FilterableField
from djing.core.Fields.Field import Field
from djing.core.Fields.FieldFilterable import FieldFilterable
from djing.core.Fields.Filters.BooleanGroupFilter import BooleanGroupFilter
from djing.core.Http.Requests.DjingRequest import DjingRequest
from django.db.models import QuerySet, Q


class BooleanGroup(Field, FieldFilterable, FilterableField):
    component = "boolean-group-field"
    _text_align = "center"
    _no_value_text = "No Data"
    _hide_true_values = None
    _hide_false_values = None
    _options = None

    def make_filter(self, request: DjingRequest):
        return BooleanGroupFilter(self)

    def options(self, options) -> Self:
        if callable(options):
            options = options()

        def map_options(label, name):
            return (
                {"label": label, "name": name}
                if isinstance(options, dict)
                else {"label": label, "name": label}
            )

        self._options = collect(options).map(map_options).values().all()

        return self

    def _default_filterable_callback(self):
        def filterable_callback(
            request: DjingRequest, query: QuerySet, value, attribute
        ):
            items = value.items() if isinstance(value, dict) else []

            if not items:
                return query

            filter_query = Q()

            for key, include in items:
                lookup = f"{attribute}__icontains"

                condition = Q(**{lookup: key})

                filter_query &= condition if include else ~condition

            return query.filter(filter_query)

        return filterable_callback

    def fill_attribute_from_request(self, request, request_attribute, model, attribute):
        if request_attribute in request.all():
            value = request.all().get(request_attribute)

            try:
                if self.has_fillable_value(value):
                    setattr(model, attribute, value)
            except:
                pass

    def hide_true_values(self) -> Self:
        self._hide_true_values = True
        self._hide_false_values = False

        return self

    def hide_false_values(self) -> Self:
        self._hide_true_values = False
        self._hide_false_values = True

        return self

    def no_value_text(self, text) -> Self:
        self._no_value_text = text

        return self

    def serialize_for_filter(self):
        def serialize_options(field):
            field["options"] = collect(field["options"]).transform(
                lambda option: {
                    "label": option.get("label"),
                    "value": option.get("name"),
                }
            )

            return Arr.only(field, ["unique_key", "options"])

        return transform(self.json_serialize(), serialize_options)

    def json_serialize(self):
        return array_merge(
            super().json_serialize(),
            {
                "hide_true_values": self._hide_true_values,
                "hide_false_values": self._hide_false_values,
                "options": self._options,
                "no_value_text": self._no_value_text,
            },
        )

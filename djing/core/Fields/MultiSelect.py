from typing import Self
from Illuminate.Collections.Arr import Arr
from Illuminate.Collections.helpers import collect
from Illuminate.Support.helpers import transform
from djing.core.Contracts.FilterableField import FilterableField
from djing.core.Fields.Field import Field
from djing.core.Fields.FieldFilterable import FieldFilterable
from djing.core.Fields.Filters.MultiSelectFilter import MultiSelectFilter
from djing.core.Http.Requests.DjingRequest import DjingRequest
from django.db.models import QuerySet, Q


class MultiSelect(Field, FieldFilterable, FilterableField):
    component = "multi-select-field"
    option_callback = None

    def _default_filterable_callback(self):
        def filterable_callback(
            request: DjingRequest, query: QuerySet, value, attribute
        ):
            items = [item for item in value if len(item) > 0]

            if not items:
                return query

            filter_query = Q()

            for item in items:
                filter_query &= Q(**{f"{attribute}__icontains": item})

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
        return MultiSelectFilter(self)

    def serialize_for_filter(self):
        return transform(
            self.json_serialize(),
            lambda field: Arr.only(
                field,
                ["unique_key", "name", "attribute", "options", "type"],
            ),
        )

    def json_serialize(self):
        self.with_meta({"options": self.serialize_options()})

        return super().json_serialize()

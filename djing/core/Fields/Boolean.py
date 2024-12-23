from typing import Self
from Illuminate.Collections.Arr import Arr
from Illuminate.Support.helpers import transform
from djing.core.Contracts.FilterableField import FilterableField
from djing.core.Fields.Field import Field
from djing.core.Fields.FieldFilterable import FieldFilterable
from djing.core.Fields.Filters.BooleanFilter import BooleanFilter
from djing.core.Http.Requests.DjingRequest import DjingRequest


class Boolean(Field, FieldFilterable, FilterableField):
    component = "boolean-field"
    _text_align = "center"
    _true_value = True
    _false_value = False

    def make_filter(self, request: DjingRequest):
        return BooleanFilter(self)

    def _resolve_attribute(self, resource, attribute):
        value = super()._resolve_attribute(resource, attribute)

        if value is None:
            return None

        try:
            return True if bool(value) == self._true_value else False
        except:
            return False

    def resolve_default_value(self, request: DjingRequest):
        if self.request_should_resolve_default_value(request):
            value = super().resolve_default_value(request)

            return value if value else False

    def true_value(self, value) -> Self:
        self._true_value = value

        return self

    def false_value(self, value) -> Self:
        self._false_value = value

        return self

    def values(self, true_value, false_value) -> Self:
        return self.true_value(true_value).false_value(false_value)

    def serialize_for_filter(self):
        return transform(
            self.json_serialize(),
            lambda field: Arr.only(field, ["unique_key"]),
        )

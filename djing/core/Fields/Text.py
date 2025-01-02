from Illuminate.Collections.Arr import Arr
from Illuminate.Support.builtins import array_merge
from Illuminate.Support.helpers import transform
from djing.core.Contracts.FilterableField import FilterableField
from djing.core.Fields.AsHtml import AsHtml
from djing.core.Fields.Copyable import Copyable
from djing.core.Fields.Field import Field
from djing.core.Fields.FieldFilterable import FieldFilterable
from djing.core.Fields.Filters.TextFilter import TextFilter
from djing.core.Http.Requests.DjingRequest import DjingRequest


class Text(Field, AsHtml, Copyable, FieldFilterable, FilterableField):
    component = "text-field"

    def make_filter(self, request: DjingRequest):
        return TextFilter(self)

    def serialize_for_filter(self):
        return transform(
            self.json_serialize(),
            lambda field: Arr.only(
                field,
                [
                    "unique_key",
                    "name",
                    "attribute",
                    "type",
                    "placeholder",
                    "extra_attributes",
                ],
            ),
        )

    def json_serialize(self):
        return array_merge(
            super().json_serialize(),
            {
                "as_html": self._as_html,
                "copyable": self._copyable,
            },
        )

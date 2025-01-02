import html
from Illuminate.Support.builtins import array_merge
from djing.core.Contracts.FilterableField import FilterableField
from djing.core.Fields.Field import Field
from djing.core.Fields.FieldFilterable import FieldFilterable
from djing.core.Fields.Filters.TextFilter import TextFilter
from djing.core.Http.Requests.DjingRequest import DjingRequest


class Textarea(Field, FieldFilterable, FilterableField):
    component = "textarea-field"
    _show_on_index = False
    rows = 5

    def make_filter(self, request: DjingRequest):
        return TextFilter(self)

    def resolve_for_display(self, resource, attribute=None):
        super().resolve_for_display(resource, attribute)

        return html.escape(self.value)

    def json_serialize(self):
        return array_merge(
            super().json_serialize(),
            {
                "rows": self.rows,
            },
        )

from Illuminate.Collections.Arr import Arr
from Illuminate.Support.builtins import array_merge
from Illuminate.Support.helpers import transform
from djing.core.Fields.Text import Text
from djing.core.Fields.Filters.TextFilter import TextFilter
from djing.core.Http.Requests.DjingRequest import DjingRequest


class Email(Text):
    component = "email-field"

    def __init__(self, name="Email", attribute="email", resolve_callback=None):
        super().__init__(name, attribute, resolve_callback)

    def make_filter(self, request: DjingRequest):
        text_filter = TextFilter(self)

        text_filter.component = "email-field"

        return text_filter

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

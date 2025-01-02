import base64
import json

from Illuminate.Collections.helpers import collect
from djing.core.Query.ApplyFilter import ApplyFilter


class FilterDecoder:
    def __init__(self, filter_string, available_filters=[]):
        self._filter_string = filter_string
        self._available_filters = collect(available_filters)

    def filters(self):
        if not self._filter_string:
            return collect([])

        filters = self.decode_from_base64_string(self._filter_string)

        def map_matching_filter(filter):
            filter_class = list(filter.keys())[0]

            filter_value = filter[filter_class]

            matching_filter = self._available_filters.first(
                lambda available_filter: available_filter.key() == filter_class
            )

            if matching_filter:
                return {"filter": matching_filter, "value": filter_value}

        def reject_unmatched_filter(filter):
            filter_value = filter["value"]

            if filter_value == "":
                return True

            return False

        items = (
            collect(filters)
            .map(map_matching_filter)
            .filter()
            .reject(reject_unmatched_filter)
            .map(lambda filter: (ApplyFilter(filter["filter"], filter["value"])))
            .values()
        )

        return items

    def decode_from_base64_string(self, filter_string):
        try:
            decoded = base64.b64decode(filter_string).decode("utf-8")

            return json.loads(decoded)
        except:
            return []

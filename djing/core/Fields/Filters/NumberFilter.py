from Illuminate.Collections.helpers import collect
from djing.core.Fields.Filters.Filter import Filter


class NumberFilter(Filter):
    component = "number-field"

    def apply(self, request, query, value):
        value = collect(value).transform(lambda value: value)

        if value.filter().is_not_empty():
            return self.field.apply_filter(request, query, value)

        return query

    def default(self):
        return [None, None]

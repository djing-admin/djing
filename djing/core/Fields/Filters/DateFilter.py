from datetime import datetime, timedelta
from Illuminate.Collections.helpers import collect
from djing.core.Fields.Filters.Filter import Filter


class DateFilter(Filter):
    component = "date-field"

    def apply(self, request, query, value):
        def transform_date(value):
            if value is not None:
                return datetime.fromisoformat(value)

            return None

        value = collect(value).transform(transform_date)

        if value.filter().is_not_empty():
            start_of_the_day = datetime(value[0].year, value[0].month, value[0].day)

            value[0] = start_of_the_day

            value[1] = start_of_the_day + timedelta(hours=23, minutes=59, seconds=59)

            return self.field.apply_filter(request, query, value)

        return query

    def default(self):
        return [None, None]

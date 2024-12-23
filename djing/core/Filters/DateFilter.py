from typing import Self
from djing.core.Filters.Filter import Filter


class DateFilter(Filter):
    component = "date-filter"

    def first_day_of_week(self, day) -> Self:
        return self.with_meta({"first_day_of_week": day})

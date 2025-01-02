import pendulum

from typing import Any, Self
from Illuminate.Support.builtins import array_merge
from django.db.models import Count, Sum, Avg, Min, Max, Model
from djing.core.Http.Requests.DjingRequest import DjingRequest
from djing.core.Metrics.RangedMetric import RangedMetric
from djing.core.Metrics.ValueResult import ValueResult
from djing.core.Util import Util


class Value(RangedMetric):
    component = "value-metric"

    _icon = "chart-bar"

    def icon(self, icon) -> Self:
        self._icon = icon

        return self

    def count(
        self, request: DjingRequest, model: Model | Any, column=None, date_column=None
    ):
        return self.aggregate(request, model, Count, column, date_column)

    def average(
        self, request: DjingRequest, model: Model | Any, column=None, date_column=None
    ):
        return self.aggregate(request, model, Avg, column, date_column)

    def sum(
        self, request: DjingRequest, model: Model | Any, column=None, date_column=None
    ):
        return self.aggregate(request, model, Sum, column, date_column)

    def max(
        self, request: DjingRequest, model: Model | Any, column=None, date_column=None
    ):
        return self.aggregate(request, model, Max, column, date_column)

    def min(
        self, request: DjingRequest, model: Model | Any, column=None, date_column=None
    ):
        return self.aggregate(request, model, Min, column, date_column)

    def aggregate(
        self,
        request: DjingRequest,
        model: Model | Any,
        function_name,
        column=None,
        date_column=None,
    ):
        try:
            queryset = self._get_queryset(request, model)

            column = column if column else Util.get_key_name(model)

            date_column = date_column if date_column else "created_at"

            range = request.query_param("range")

            timezone = request.query_param("timezone")

            if range == "ALL":
                return self.results(queryset, function_name, column)

            current_start_range, current_end_range = self.current_range(range, timezone)

            current_payload = {
                f"{date_column}__range": (current_start_range, current_end_range)
            }

            current_queryset = queryset.filter(**current_payload)

            current_results = self.results(current_queryset, function_name, column)

            previous_start_range, previous_end_range = self.previous_range(
                range, timezone
            )

            previous_payload = {
                f"{date_column}__range": (previous_start_range, previous_end_range)
            }

            previous_queryset = queryset.filter(**previous_payload)

            previous_results = self.results(previous_queryset, function_name, column)

            return ValueResult(current_results).previous(previous_results)
        except Exception as e:
            print("e", e)

    def results(self, queryset, function_name, column):
        results = queryset.aggregate(data=function_name(column))

        return results["data"]

    def current_range(self, range, timezone):
        now = pendulum.now(timezone)

        start, end = None, None

        if range == "TODAY":
            start, end = now.start_of("day"), now.end_of("day")
        elif range == "YESTERDAY":
            start, end = now.subtract(days=1).start_of("day"), now.subtract(
                days=1
            ).end_of("day")
        elif range == "THIS_WEEK":
            start, end = now.start_of("week"), now.end_of("week")
        elif range == "MTD":
            start, end = now.start_of("month"), now
        elif range == "QTD":
            start, end = now.start_of("quarter"), now
        elif range == "YTD":
            start, end = now.start_of("year"), now
        else:
            try:
                start, end = now.subtract(days=int(range)), now
            except ValueError:
                raise ValueError(f"Invalid range: {range}")

        return start, end

    def previous_range(self, range, timezone):
        now = pendulum.now(timezone)

        start, end = None, None

        if range == "TODAY":
            start, end = now.subtract(days=1).start_of("day"), now.subtract(
                days=1
            ).end_of("day")
        elif range == "YESTERDAY":
            start, end = now.subtract(days=2).start_of("day"), now.subtract(
                days=2
            ).end_of("day")
        elif range == "THIS_WEEK":
            start, end = now.subtract(weeks=1).start_of("week"), now.subtract(
                weeks=1
            ).end_of("week")
        elif range == "MTD":
            start, end = now.subtract(months=1).start_of("month"), now.subtract(
                months=1
            )
        elif range == "QTD":
            start, end = now.subtract(months=1).start_of("quarter"), now.subtract(
                months=1
            )
        elif range == "YTD":
            start, end = now.subtract(years=1).start_of("year"), now.subtract(years=1)
        else:
            try:
                start, end = now.subtract(days=int(range) * 2), now.subtract(
                    days=int(range)
                ).subtract(seconds=1)
            except ValueError:
                raise ValueError(f"Invalid range: {range}")

        return start, end

    def json_serialize(self):
        return array_merge(
            super().json_serialize(),
            {
                "icon": self._icon,
            },
        )

from datetime import datetime
from typing import Any
from django.db.models import Count, Sum, Avg, Min, Max, Model
from djing.core.Http.Requests.DjingRequest import DjingRequest
from djing.core.Metrics.Metric import Metric
from djing.core.Metrics.PartitionResult import PartitionResult
from djing.core.Util import Util


class Partition(Metric):
    component = "partition-metric"

    def count(
        self,
        request: DjingRequest,
        model: Model | Any,
        group_by_column: str,
        column=None,
    ):
        return self.aggregate(request, model, Count, column, group_by_column)

    def average(
        self,
        request: DjingRequest,
        model: Model | Any,
        group_by_column: str,
        column=None,
    ):
        return self.aggregate(request, model, Avg, column, group_by_column)

    def sum(
        self,
        request: DjingRequest,
        model: Model | Any,
        group_by_column: str,
        column=None,
    ):
        return self.aggregate(request, model, Sum, column, group_by_column)

    def max(
        self,
        request: DjingRequest,
        model: Model | Any,
        group_by_column: str,
        column=None,
    ):
        return self.aggregate(request, model, Max, column, group_by_column)

    def min(
        self,
        request: DjingRequest,
        model: Model | Any,
        group_by_column: str,
        column=None,
    ):
        return self.aggregate(request, model, Min, column, group_by_column)

    def aggregate(
        self,
        request: DjingRequest,
        model: Model | Any,
        function_name,
        column: str | None = None,
        group_by_column: str | None = None,
    ):
        try:
            queryset = self._get_queryset(request, model)

            column = column if column else Util.get_key_name(model)

            total_results = self.results(
                queryset, function_name, column, group_by_column
            )

            return total_results
        except Exception as e:
            print("e", e)

    def results(self, queryset, function_name, column, group_by_column):
        total = queryset.count()

        results = queryset.values(group_by_column).annotate(data=function_name(column))

        return PartitionResult(results, total, group_by_column, self.label)

    def label(self, value: datetime | bool | int | float | str):
        if isinstance(value, datetime):
            return value.strftime("%Y-%m-%d %H:%M:%S")

        if isinstance(value, bool):
            return 1 if value == True else 0

        return str(value)

from typing import Any, Callable
from Illuminate.Helpers.Util import Util as HelpersUtil
from django.db.models import Count, Model
from djing.core.Http.Requests.DjingRequest import DjingRequest
from djing.core.Metrics.Metric import Metric
from djing.core.Metrics.ProgressResult import ProgressResult
from djing.core.Util import Util


class Progress(Metric):
    component = "progress-metric"

    def count(
        self,
        request: DjingRequest,
        model: Model | Any,
        progress: Callable[..., Any],
        column=None,
        target=None,
    ):
        return self.aggregate(request, model, Count, column, progress, target)

    def sum(
        self,
        request: DjingRequest,
        model: Model | Any,
        progress: Callable[..., Any],
        column=None,
        target=None,
    ):
        return self.aggregate(request, model, Count, column, progress, target)

    def aggregate(
        self,
        request: DjingRequest,
        model: Model | Any,
        function_name,
        column: str,
        progress: Callable[..., Any],
        target: Any,
    ):
        try:
            queryset = self._get_queryset(request, model)

            column = column if column else Util.get_key_name(model)

            current_queryset = HelpersUtil.callback_with_dynamic_args(
                progress, [queryset]
            )

            current_results = self.results(current_queryset, function_name, column)

            return ProgressResult(current_results, target)
        except Exception as e:
            print("e", e)

    def results(self, queryset, function_name, column):
        results = queryset.aggregate(data=function_name(column))

        return results["data"]

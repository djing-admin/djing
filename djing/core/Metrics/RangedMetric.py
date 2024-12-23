from typing import Self
from Illuminate.Support.builtins import array_merge
from djing.core.Metrics.Metric import Metric


class RangedMetric(Metric):
    _ranges: dict = {}
    _selected_range_key = None

    def ranges(self) -> dict:
        return self._ranges

    def default_range(self, key) -> Self:
        self._selected_range_key = key

        return self

    def json_serialize(self):
        return array_merge(
            super().json_serialize(),
            {
                "selected_range_key": self._selected_range_key,
                "ranges": [
                    {"label": value, "value": key}
                    for key, value in self.ranges().items()
                ],
            },
        )

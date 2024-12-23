from typing import Self
from Illuminate.Support.builtins import array_merge
from djing.core.Metrics.Metric import Metric


class Table(Metric):
    component = "table-metric"

    _empty_text = "No Results found..."

    def empty_text(self, text: str) -> Self:
        self._empty_text = text

        return self

    def json_serialize(self):
        return array_merge(
            super().json_serialize(),
            {
                "empty_text": self._empty_text,
            },
        )

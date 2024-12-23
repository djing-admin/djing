from typing import Self
from Illuminate.Collections.Arr import Arr
from Illuminate.Collections.helpers import collect
from Illuminate.Support.builtins import array_merge
from Illuminate.Support.helpers import transform
from djing.core.Fields.Field import Field
from djing.core.Fields.Filters.NumberFilter import NumberFilter
from djing.core.Fields.Text import Text
from djing.core.Http.Requests.DjingRequest import DjingRequest
from django.db.models import QuerySet, Q


class Number(Text):
    component = "number-field"

    _min = None
    _max = None
    _step = None

    def __init__(self, name, attribute=None, resolve_callback=None):
        super().__init__(name, attribute, resolve_callback)

        self.text_align(Field.RIGHT_ALIGN).with_meta({"type": "number"}).display_using(
            lambda value: str(value) if value else None
        )

    def min(self, min: int) -> Self:
        self._min = min

        return self

    def max(self, max: int) -> Self:
        self._max = max

        return self

    def step(self, step: int) -> Self:
        self._step = step

        return self

    def make_filter(self, request: DjingRequest):
        return NumberFilter(self)

    def _default_filterable_callback(self):
        def filterable_callback(
            request: DjingRequest, query: QuerySet, value, attribute
        ):
            min_value, max_value = value[0], value[1]

            filter_query = Q()

            if min_value and max_value:
                filter_query = Q(**{f"{attribute}__gte": min_value}) & Q(
                    **{f"{attribute}__lte": max_value}
                )

            elif min_value and not max_value:
                filter_query = Q(**{f"{attribute}__gte": min_value})

            elif max_value and not min_value:
                filter_query = Q(**{f"{attribute}__lte": max_value})

            if filter_query:
                return query.filter(filter_query)

            return query

        return filterable_callback

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
                    "min",
                    "max",
                    "step",
                    "placeholder",
                    "extra_attributes",
                ],
            ),
        )

    def json_serialize(self):
        data = (
            collect(
                {
                    "min": self._min,
                    "max": self._max,
                    "step": self._step,
                }
            )
            .reject(lambda value: not value)
            .all()
        )

        return array_merge(
            super().json_serialize(),
            dict(data),
        )

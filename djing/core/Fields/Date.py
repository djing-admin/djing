from datetime import date, datetime
from typing import Self
from Illuminate.Collections.Arr import Arr
from Illuminate.Support.builtins import array_merge
from Illuminate.Support.helpers import transform
from djing.core.Contracts.FilterableField import FilterableField
from djing.core.Fields.Field import Field
from djing.core.Fields.FieldFilterable import FieldFilterable
from djing.core.Fields.Filters.DateFilter import DateFilter
from djing.core.Http.Requests.DjingRequest import DjingRequest
from django.db.models import QuerySet, Q


class Date(Field, FieldFilterable, FilterableField):
    component = "date-field"

    _min = None
    _max = None
    _step = 1

    def __init__(self, name, attribute=None, resolve_callback=None):
        super().__init__(
            name,
            attribute,
            resolve_callback if resolve_callback else self._get_resolve_callback,
        )

    def make_filter(self, request: DjingRequest):
        return DateFilter(self)

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

    def min(self, value) -> Self:
        if not isinstance(value, (str, date, datetime)):
            raise Exception("Must be a date instance")

        if isinstance(value, str):
            try:
                self._min = datetime.fromisoformat(value).strftime("%Y-%m-%d")
            except:
                raise Exception("Must be a date instance")

        self._min = value.strftime("%Y-%m-%d")

        return self

    def max(self, value) -> Self:
        if not isinstance(value, (str, date, datetime)):
            raise Exception("Must be a date instance")

        if isinstance(value, str):
            try:
                self._max = datetime.fromisoformat(value).strftime("%Y-%m-%d")
            except:
                raise Exception("Must be a date instance")

        self._max = value.strftime("%Y-%m-%d")

        return self

    def step(self, step) -> Self:
        self._step = step

        return self

    def resolve_default_value(self, request: DjingRequest):
        value = super().resolve_default_value(request)

        return self._get_resolve_callback(value)

    def _get_resolve_callback(self, value):
        if value is not None:
            if not isinstance(value, (str, date, datetime)):
                raise Exception("Must be a date instance")

            if isinstance(value, str):
                try:
                    value = datetime.fromisoformat(value)
                except:
                    raise Exception("Must be a date instance")

            return value.strftime("%Y-%m-%d")

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
                    "placeholder",
                    "extra_attributes",
                ],
            ),
        )

    def json_serialize(self):
        return array_merge(
            super().json_serialize(),
            {
                "min": self._min,
                "max": self._max,
                "step": self._step,
            },
        )

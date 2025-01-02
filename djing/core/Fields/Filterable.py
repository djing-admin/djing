from abc import abstractmethod
from typing import Callable, Optional, Self
from Illuminate.Helpers.Util import Util
from djing.core.Http.Requests.DjingRequest import DjingRequest
from django.db.models import QuerySet


class Filterable:
    _filterable_callback = None

    def filterable(self, callback: Optional[Callable] = None) -> Self:
        if callback:
            self._filterable_callback = callback
        else:
            self._filterable_callback = self._default_filterable_callback()

        return self

    def apply_filter(self, request: DjingRequest, query: QuerySet, value):
        attribute = self._filterable_attribute()

        return Util.callback_with_dynamic_args(
            self._filterable_callback, [request, query, value, attribute]
        )

    def resolve_filter(self, request: DjingRequest):
        return (
            self.make_filter(request) if callable(self._filterable_callback) else None
        )

    def _default_filterable_callback(self):
        def filterable_callback(
            request: DjingRequest, query: QuerySet, value, attribute
        ):
            return query.filter(**{attribute: value})

        return filterable_callback

    def _filterable_attribute(self):
        return self.attribute

    def serialize_for_filter(self):
        return self.json_serialize()

    @abstractmethod
    def make_filter(self, request: DjingRequest):
        pass

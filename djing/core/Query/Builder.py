from typing import Any, Callable, List, Optional, Self, Tuple, Type
from django.db.models import base, QuerySet, Q
from djing.core.Resource import Resource
from djing.core.Util import Util
from djing.core.Http.Requests.DjingRequest import DjingRequest
from djing.core.Query.SimplePaginator import SimplePaginator


class Builder:
    def __init__(self, resource_class: Type[Resource]):
        self._resource_class = resource_class

        self._model: base.Model = self._resource_class.new_model()

        self._model_pk = Util.get_key_name(self._model)

    def where_key(self, query: QuerySet, key: int) -> QuerySet:
        return self._resource_class.get_queryset().filter(**{self._model_pk: key})

    def search(
        self,
        request: DjingRequest,
        query: QuerySet,
        search: Optional[Any] = None,
        filters: List[Any] = [],
        orderings: List[Any] = [],
    ):
        self._request = request

        self._query = query

        self._set_query(search, filters, orderings)

        paginator = self._get_paginator()

        return paginator

    def _set_query(self, search, filters, orderings) -> QuerySet:
        return (
            self._apply_search(search)
            ._apply_filters(filters)
            ._apply_orderings(orderings)
        )

    def _apply_search(self, search) -> Self:
        try:
            if not search:
                return self

            searchable_fields = self._get_searchable_fields()

            query = Q()

            for searchable_field in searchable_fields:
                query |= Q(**{f"{searchable_field}__icontains": search})

            self._query = self._query.filter(query)
        except Exception as e:
            print(f"error applying search", e)

        return self

    def _apply_filters(self, filters: List[Tuple[int, Callable[..., Any]]]) -> Self:
        try:
            for _, filter in filters:
                self._query = filter(self._request, self._query)
        except Exception as e:
            print(f"error applying filters", e)

        return self

    def _apply_orderings(self, orderings) -> Self:
        try:
            if not orderings:
                return self

            order_by, order_by_direction = orderings

            self._query = self._query.order_by(
                f"-{order_by}" if order_by_direction == "desc" else order_by
            )
        except Exception as e:
            print(f"error applying orderings", e)

        return self

    def _get_paginator(self) -> QuerySet:
        return SimplePaginator(query=self._query, request=self._request)

    def _get_searchable_fields(self):
        default_columns = self._resource_class.searchable_columns()

        return getattr(self._resource_class, "search", default_columns)

from typing import TYPE_CHECKING, Any, List, Optional, Protocol, Self
from django.db.models import QuerySet

if TYPE_CHECKING:
    from djing.core.Http.Requests.DjingRequest import DjingRequest
    from djing.core.Query.SimplePaginator import SimplePaginator


class QueryBuilder(Protocol):
    def search(
        self,
        request: "DjingRequest",
        query,
        search: Optional[Any] = None,
        filters: List[Any] = [],
        orderings: List[Any] = [],
    ) -> "SimplePaginator":
        pass

    def paginate(self, per_page: int) -> Self:
        pass

    def where_key(self, query: QuerySet, key: int) -> QuerySet:
        pass

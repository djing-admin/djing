from typing import Self

from djing.core.Http.Requests.DjingRequest import DjingRequest


class Searchable:
    _searchable = False

    def searchable(self, searchable=True) -> Self:
        self._searchable = searchable

        return self

    def is_searchable(self, request: DjingRequest) -> bool:
        return self._searchable() if callable(self._searchable) else self._searchable

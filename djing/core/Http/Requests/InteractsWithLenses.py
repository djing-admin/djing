from typing import TYPE_CHECKING
from Illuminate.Exceptions.RouteNotFoundException import RouteNotFoundException
from Illuminate.Exceptions.UnauthorizedAccessException import (
    UnauthorizedAccessException,
)
from django.db.models import QuerySet
from djing.core.Resource import Resource

if TYPE_CHECKING:
    from djing.core.Lenses.Lens import Lens


class InteractsWithLenses:
    def lens(self) -> "Lens":
        if not self.lens_exists():
            raise RouteNotFoundException()

        available_lenses = self.available_lenses()

        return available_lenses.first(
            lambda lens: lens.uri_key() == self.route_param("lens")
        )

    def available_lenses(self):
        resource: Resource = self.new_resource()

        if not resource.authorized_to_view_any(self):
            raise UnauthorizedAccessException()

        return resource.available_lenses(self)

    def lens_exists(self):
        resource: Resource = self.new_resource()

        lenses = resource.resolve_lenses(self)

        return (
            lenses.first(lambda lens: lens.uri_key() == self.route_param("lens"))
            is not None
        )

    def new_search_query(self) -> QuerySet:
        lens = self.lens()

        query: QuerySet = lens.query(self, self.new_query())

        return query

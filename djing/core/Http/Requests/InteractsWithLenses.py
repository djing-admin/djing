from typing import TYPE_CHECKING
from Illuminate.Exceptions.RouteNotFoundException import RouteNotFoundException
from Illuminate.Exceptions.UnauthorizedAccessException import (
    UnauthorizedAccessException,
)

from djing.core.Resource import Resource

if TYPE_CHECKING:
    from djing.core.Lenses.Lens import Lens


class InteractsWithLenses:
    def lens(self) -> "Lens":
        if not self.lens_exists():
            raise RouteNotFoundException()

        return self.available_lenses().first(
            lambda lens: lens.uri_key() == self.query_param("lens")
        )

    def available_lenses(self):
        resource: Resource = self.new_resource()

        if not resource.authorized_to_view_any(self):
            raise UnauthorizedAccessException()

        return resource.available_lenses(self)

    def lens_exists(self):
        resource: Resource = self.new_resource()

        return (
            resource.resolve_lenses(self).first(
                lambda lens: lens.uri_key() == self.query_param("lens")
            )
            is not None
        )

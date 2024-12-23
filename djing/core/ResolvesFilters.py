from Illuminate.Collections.Collection import Collection
from Illuminate.Collections.helpers import collect
from Illuminate.Support.builtins import array_values
from djing.core.Http.Requests.DjingRequest import DjingRequest


class ResolvesFilters:
    def available_filters(self, request: DjingRequest):
        items = (
            self.resolve_filters(request)
            .concat(self.resolve_filters_from_fields(request))
            .filter(lambda filter: filter.authorized_to_see(request))
            .values()
        )

        return items

    def resolve_filters(self, request: DjingRequest):
        return collect(array_values(self.filters(request)))

    def resolve_filters_from_fields(self, request: DjingRequest):
        filterable_fields: Collection = self.filterable_fields(request)

        items = (
            filterable_fields.transform(lambda field: field.resolve_filter(request))
            .filter()
            .all()
        )

        return collect(array_values(items))

    def filters(self, request: DjingRequest):
        return []

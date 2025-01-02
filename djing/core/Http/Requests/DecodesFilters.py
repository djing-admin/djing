from Illuminate.Collections.Collection import Collection
from djing.core.Filters.FilterDecoder import FilterDecoder
from djing.core.Resource import Resource


class DecodesFilters:
    def filters(self) -> Collection:
        available_filters = self.available_filters()

        filter_string = self.query_param("filter")

        return FilterDecoder(filter_string, available_filters).filters()

    def available_filters(self):
        resource: Resource = self.new_resource()

        return resource.available_filters(self)

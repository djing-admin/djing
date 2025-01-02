from Illuminate.Collections.helpers import collect
from Illuminate.Support.Facades.App import App
from djing.core.Filters.Filter import Filter
from djing.core.Http.Requests.DjingRequest import DjingRequest


class BooleanFilter(Filter):
    component = "boolean-filter"

    def default(self):
        return (
            collect(self.options(App.make(DjingRequest)))
            .values()
            .map_with_keys(lambda option: {option: False})
            .all()
        )

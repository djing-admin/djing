from Illuminate.Collections.helpers import collect
from Illuminate.Support.builtins import array_values
from djing.core.Http.Requests.DjingRequest import DjingRequest


class ResolvesLenses:
    def available_lenses(self, request: DjingRequest):
        return (
            self.resolve_lenses(request)
            .filter(lambda lens: lens.authorized_to_see(request))
            .values()
        )

    def resolve_lenses(self, request: DjingRequest):
        return collect(array_values(self.lenses(request)))

    def lenses(self, request: DjingRequest):
        return []

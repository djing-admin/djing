from Illuminate.Collections.Collection import Collection
from djing.core.Http.Requests.DjingRequest import DjingRequest
from djing.core.Facades.Djing import Djing


class DashboardRequest(DjingRequest):
    def available_cards(self, key) -> Collection:
        return Djing.available_dashboard_cards_for_dashboard(key, self)

from Illuminate.Collections.helpers import collect
from djing.core.Http.Requests.DjingRequest import DjingRequest
from djing.core.Facades.Djing import Djing
from djing.core.HasMenu import HasMenu

from djing.core.Menu.MenuSection import MenuSection
from djing.core.Tool import Tool


class Dashboard(Tool, HasMenu):
    def menu(self, request: DjingRequest):
        available_dashboards = Djing.available_dashboards(request)

        collection = collect(available_dashboards)

        if collection.count() > 1:
            return (
                MenuSection.make(
                    "Dashboard",
                    collection.map(lambda dashboard: dashboard.menu(request)),
                )
                .collapsable()
                .with_icon("view-grid")
            )

        if collection.count() == 1:
            first_dashboard = collection.first()

            items = (
                MenuSection.make(
                    first_dashboard.label(),
                    collection,
                )
                .path(f"/dashboards/{first_dashboard.uri_key()}")
                .with_icon("view-grid")
            )

            return items

from Illuminate.Collections.Collection import Collection
from djing.core.Http.Requests.DjingRequest import DjingRequest
from djing.core.Makeable import Makeable


class ActionCollection(Collection, Makeable):
    def authorized_to_see_on_table_row(self, request: DjingRequest):
        return self.filter(lambda action: action.shown_on_table_row()).filter(
            lambda action: action.authorized_to_see(request)
        )

    def authorized_to_see_on_index(self, request: DjingRequest):
        def authorized_to_see(action):
            if action._sole:
                return (
                    not request.all_resources_selected()
                    and len(request.selected_resource_ids()) == 1
                    and action.authorized_to_see(request)
                )

            return action.authorized_to_see(request)

        return self.filter(lambda action: action.shown_on_index()).filter(
            authorized_to_see
        )

    def authorized_to_see_on_detail(self, request: DjingRequest):
        return self.filter(lambda action: action.shown_on_detail()).filter(
            lambda action: action.authorized_to_see(request)
        )

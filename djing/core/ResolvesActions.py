from django.db.models import base
from Illuminate.Support.builtins import array_merge
from djing.core.Actions.ActionCollection import ActionCollection
from djing.core.Http.Requests.DjingRequest import DjingRequest


class ResolvesActions:
    def resolve_actions(self, request: DjingRequest):
        return ActionCollection.make(self.actions(request))

    def actions(self, request: DjingRequest):
        return self.defaults_with([])

    @classmethod
    def defaults_with(cls, actions):
        return array_merge(cls.default_actions(), actions)

    @classmethod
    def default_actions(cls):
        return []

    def available_actions(self, request: DjingRequest):
        return []

    def available_actions_on_index(self, request: DjingRequest):
        resource: base.Model = self.resource

        actions = self.resolve_actions(request).authorized_to_see_on_index(request)

        def authorized_to_run(action):
            action.authorized_to_run(request, self.resource)

        if resource and hasattr(resource, "id"):
            return actions.each(authorized_to_run).values()

        return actions.values()

    def available_actions_on_detail(self, request: DjingRequest):
        def authorized_to_run(action):
            action.authorized_to_run(request, self.resource)

        return (
            self.resolve_actions(request)
            .authorized_to_see_on_detail(request)
            .each(authorized_to_run)
            .values()
        )

    def available_actions_on_table_row(self, request: DjingRequest):
        def authorized_to_run(action):
            action.authorized_to_run(request, self.resource)

        return (
            self.resolve_actions(request)
            .authorized_to_see_on_table_row(request)
            .each(authorized_to_run)
            .values()
        )

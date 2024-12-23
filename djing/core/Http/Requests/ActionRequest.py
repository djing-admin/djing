from typing import Optional, Type
from Illuminate.Collections.helpers import collect
from Illuminate.Exceptions.RouteNotFoundException import RouteNotFoundException
from Illuminate.Exceptions.UnauthorizedAccessException import (
    UnauthorizedAccessException,
)
from djing.core.Actions.Action import Action
from djing.core.Fields.ActionFields import ActionFields
from djing.core.Fields.FieldCollection import FieldCollection
from djing.core.Http.Requests.DjingRequest import DjingRequest
from djing.core.Http.Requests.QueriesResources import QueriesResources
from djing.core.Resource import Resource


class ActionRequest(QueriesResources, DjingRequest):
    request_name = "ActionRequest"

    current_action: Optional[Action] = None

    def action(self) -> Action:
        if self.current_action:
            return self.current_action

        resources = self.query_param("resources")

        action: Action | None = (
            self.available_actions()
            .filter(lambda action: True if resources else action.is_standalone())
            .first(lambda action: action.uri_key() == self.query_param("action"))
        )

        if action:
            self.current_action = action

            return self.current_action

        raise (
            RouteNotFoundException("action not found")
            if self.action_exists()
            else UnauthorizedAccessException("not authorized to run action")
        )

    def validate_fields(self):
        return self.action().validate_fields(self)

    def resolve_fields(self, request: DjingRequest):
        fields = request.model()

        results = (
            FieldCollection.make(self.action().fields(request))
            .authorized(request)
            .without_readonly(self)
            .without_unfillable()
            .map_with_keys(
                lambda field: {field.attribute: field.fill_for_action(self, fields)}
            )
        )

        attributes = collect(
            {
                field.column: getattr(fields, field.column)
                for field in fields._meta.fields
                if field.column in request.all().keys()
            }
        )

        return ActionFields(attributes, results.filter(lambda field: callable(field)))

    def resolve_actions(self):
        return self.new_resource().resolve_actions(self)

    def available_actions(self):
        return (
            self.resolve_actions()
            .filter(lambda action: action.authorized_to_see(self))
            .values()
        )

    def action_exists(self) -> bool:
        return (
            self.resolve_actions().first(
                lambda action: action.uri_key() == self.query_param("action")
            )
            is not None
        )

    def chunks(self, count, callback):
        models = self.to_selected_resource_query()

        return callback(models)

    def to_selected_resource_query(self):
        if self.all_resources_selected():
            return self.new_query()
        else:
            resource: Type[Resource] = self.resource()

            return resource.get_queryset().filter(id__in=self.selected_resource_ids())

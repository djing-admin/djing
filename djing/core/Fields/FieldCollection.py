from typing import Any, Self
from Illuminate.Collections.Collection import Collection
from Illuminate.Contracts.Resolvable import Resolvable
from djing.core.Contracts.ListableField import ListableField
from djing.core.Fields.FieldFilterable import FieldFilterable
from djing.core.Fields.ID import ID
from djing.core.Fields.Unfillable import Unfillable
from djing.core.Http.Requests.DjingRequest import DjingRequest
from djing.core.Makeable import Makeable
from djing.core.Panel import Panel
from djing.core.ResourceTool import ResourceTool
from djing.core.ResourceToolElement import ResourceToolElement
from djing.core.Util import Util


class FieldCollection(Collection, Makeable):
    def where_instance_of(self, instance: Any) -> Self:
        return self.filter(lambda item: isinstance(item, instance))

    def filter_for_index(self, request: DjingRequest, resource) -> Self:
        return self.filter(
            lambda field: field.is_shown_on_index(request, resource)
        ).values()

    def filter_for_detail(self, request: DjingRequest, resource) -> Self:
        return self.filter(
            lambda field: field.is_shown_on_detail(request, resource)
        ).values()

    def only_create_fields(self, request: DjingRequest, resource) -> Self:
        return self.reject(
            lambda field: (
                isinstance(field, (ResourceTool, ResourceToolElement))
                or field.attribute == "ComputedField"
                or (
                    isinstance(field, ID)
                    and field.attribute == Util.get_key_name(resource)
                )
                or not field.is_shown_on_creation(request)
            )
        )

    def only_update_fields(self, request: DjingRequest, resource) -> Self:
        return self.reject(
            lambda field: (
                isinstance(field, (ResourceTool, ResourceToolElement))
                or field.attribute == "ComputedField"
                or (
                    isinstance(field, ID)
                    and field.attribute == Util.get_key_name(resource)
                )
                or not field.is_shown_on_update(request, resource)
            )
        )

    def authorized(self, request: DjingRequest) -> Self:
        return self.filter(lambda field: field.authorize(request)).values()

    def without_listable_fields(self) -> Self:
        return self.reject(lambda field: isinstance(field, ListableField))

    def without_readonly(self, request: DjingRequest) -> Self:
        return self.reject(lambda field: field.is_readonly(request))

    def without_unfillable(self) -> Self:
        return self.reject(lambda field: isinstance(field, Unfillable))

    def resolve(self, resource):
        def should_resolve_field(field):
            if isinstance(field, Resolvable):
                field.resolve(resource)

        return self.each(should_resolve_field)

    def resolve_for_display(self, resource) -> Self:
        def resolve(field):
            field.resolve_for_display(resource)

            return True

        return self.each(resolve)

    def with_only_filterable_fields(self):
        return self.filter(
            lambda field: (
                isinstance(field, FieldFilterable)
                and field.attribute != "ComputedField"
            )
        )

    def assign_default_panel(self, label: str) -> Self:
        Panel(label, self.filter(lambda field: not field.panel))

        return self

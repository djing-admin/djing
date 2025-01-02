from typing import Any, List
from Illuminate.Collections.Collection import Collection
from Illuminate.Collections.helpers import collect, value
from Illuminate.Support.builtins import array_values
from Illuminate.Support.helpers import tap
from djing.core.Contracts.BehavesAsPanel import BehavesAsPanel
from djing.core.Contracts.Downloadable import Downloadable
from djing.core.Fields.FieldCollection import FieldCollection
from djing.core.Http.Requests.DjingRequest import DjingRequest
from djing.core.Http.Resources.Resource import Resource
from djing.core.Panel import Panel


class ResolvesFields:
    def index_fields(self, request: DjingRequest) -> FieldCollection:
        items = (
            self.available_fields(request)
            .filter_for_index(request, self.resource)
            .without_listable_fields()
            .authorized(request)
            .resolve_for_display(self.resource)
        )

        return items

    def available_fields(self, request: DjingRequest) -> FieldCollection:
        fields_method = self.fields_method(request)

        fields = getattr(self, fields_method)(request)

        return FieldCollection(fields)

    def filterable_fields(self, request: DjingRequest) -> FieldCollection:
        return (
            self.available_fields_on_index_or_detail(request)
            .with_only_filterable_fields()
            .unique(lambda field: field.attribute)
            .authorized(request)
        )

    def downloadable_fields(self, request: DjingRequest) -> FieldCollection:
        return (
            self.available_fields_on_index_or_detail(request)
            .where_instance_of(Downloadable)
            .unique(lambda field: field.attribute)
            .authorized(request)
            .resolve_for_display(self.resource)
        )

    def available_fields_on_index_or_detail(
        self, request: DjingRequest
    ) -> FieldCollection:
        return self.build_available_fields(
            request, ["field_for_index", "field_for_detail"]
        )

    def build_available_fields(self, request: DjingRequest, methods: List[str]):
        fields = collect(
            [getattr(self, "fields")(request) if hasattr(self, "fields") else []]
        )

        (
            collect(methods)
            .filter(lambda method: method != "fields" and hasattr(self, method))
            .each(lambda method: fields.push(getattr(self, method)(request)))
        )

        return FieldCollection.make(fields.flatten().to_list())

    def fields_method(self, request: DjingRequest) -> str:
        if request.is_resource_index_request() and hasattr(request, "field_for_index"):
            return "field_for_index"

        return "fields"

    def creation_fields_within_panels(self, request: DjingRequest):
        return self.creation_fields(request).assign_default_panel(
            Panel.default_name_for_create(request.new_resource())
        )

    def available_panels_for_create(
        self, request: DjingRequest, fields: FieldCollection = None
    ) -> List[Any]:
        fields_method = self.fields_method(request)

        if not fields:
            field_collection = FieldCollection.make(
                value(lambda: array_values(getattr(self, fields_method)(request)))
            )

            fields = field_collection.only_create_fields(
                request, request.new_resource()
            )

        items = self.resolve_panels_from_fields(
            request,
            fields,
            Panel.default_name_for_create(request.new_resource()),
        )

        return items.all()

    def creation_fields(self, request: DjingRequest) -> FieldCollection:
        items = (
            self.available_fields(request)
            .authorized(request)
            .only_create_fields(request, self.resource)
            .resolve(self.resource)
        )

        return items

    def update_fields_within_panels(self, request: DjingRequest, resource: Resource):
        return self.update_fields(request).assign_default_panel(
            Panel.default_name_for_update(
                resource if resource else request.new_resource()
            )
        )

    def available_panels_for_update(
        self, request: DjingRequest, resource: Resource, fields: FieldCollection = None
    ) -> List[Any]:
        fields_method = self.fields_method(request)

        if not fields:
            field_collection = FieldCollection.make(
                value(lambda: array_values(getattr(self, fields_method)(request)))
            )

            fields = field_collection.only_update_fields(request, resource)

        items = self.resolve_panels_from_fields(
            request,
            fields,
            Panel.default_name_for_update(resource),
        )

        return items.all()

    def detail_fields_within_panels(self, request: DjingRequest, resource: Resource):
        return self.detail_fields(request).assign_default_panel(
            Panel.default_name_for_detail(resource)
        )

    def available_panels_for_detail(
        self, request: DjingRequest, resource: Resource, fields: FieldCollection
    ) -> List[Any]:
        items = self.resolve_panels_from_fields(
            request,
            fields,
            Panel.default_name_for_detail(resource),
        )

        return items.all()

    def update_fields(self, request: DjingRequest) -> FieldCollection:
        return self.resolve_fields(request).only_update_fields(request, self.resource)

    def detail_fields(self, request: DjingRequest) -> FieldCollection:
        return (
            self.available_fields(request)
            .filter_for_detail(request, self.resource)
            .authorized(request)
            .resolve_for_display(self.resource)
        )

    def resolve_panels_from_fields(
        self, request: DjingRequest, fields: FieldCollection, label: str
    ) -> FieldCollection:
        def check_panel(field):
            if isinstance(field, BehavesAsPanel):
                field.as_panel()

        [default_fields, fields_with_panels] = fields.each(check_panel).partition(
            lambda field: field.panel is None
        )

        panels = (
            fields_with_panels.group_by(lambda field: field.panel)
            .transform(lambda fields, name: Panel.mutate(name, fields))
            .to_base()
        )

        return self.panels_with_default_label(
            panels,
            default_fields.values(),
            label,
        )

    def panels_with_default_label(
        self, panels: Collection, fields: FieldCollection, label: str
    ):
        def tap_panel(panel: Panel):
            if panel:
                panel.with_toolbar()

        return (
            panels.values()
            .when(
                panels.filter(lambda panel: panel.name == label).is_empty(),
                lambda panels: (
                    panels.prepend(
                        Panel.make(label, fields).with_meta({"fields": fields})
                    )
                    if fields.is_not_empty()
                    else panels
                ),
            )
            .tap(lambda panels: tap(panels.first(), tap_panel))
        )

    def resolve_fields(self, request: DjingRequest, filter=None):
        fields = self.available_fields(request).authorized(request)

        if filter:
            fields = filter(fields)

        fields.resolve(self.resource)

        return fields

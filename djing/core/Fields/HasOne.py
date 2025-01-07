from Illuminate.Support.builtins import array_merge
from djing.core.Contracts.BehavesAsPanel import BehavesAsPanel
from djing.core.Contracts.FilterableField import FilterableField
from djing.core.Contracts.RelatableField import RelatableField
from djing.core.Fields.Field import Field
from djing.core.Fields.ID import ID
from djing.core.Http.Requests.DjingRequest import DjingRequest
from djing.core.Panel import Panel
from djing_admin.app.Djing.Resource import Resource


class HasOne(Field, BehavesAsPanel, RelatableField):
    component = "has-one-field"

    def __init__(self, name, attribute=None, resource=None):
        super().__init__(name, attribute)

        if not resource or not issubclass(resource, Resource):
            raise Exception("Invalid Djing Resource")

        if not attribute:
            raise Exception("Invalid Resource attribute")

        self.resource_class = resource
        self.resource_name = resource.uri_key()
        self.attribute = attribute
        self.has_one_relationship = attribute
        self.singular_label = name
        self.has_one_id = None

    def as_panel(self):
        return (
            Panel.make(self.name, [self])
            .with_meta({"prefix_component": True})
            .help(self._help_text)
            .with_component("relationship-panel")
        )

    def is_shown_on_index(self, request, resource):
        return False

    def relationship_name(self):
        return self.has_one_relationship

    def relationship_type(self):
        return "has_one"

    def authorize(self, request: DjingRequest):
        if hasattr(self.resource_class, "authorized_to_view_any"):
            return super().authorize(request)

    def _format_display_value(self, resource):
        if not isinstance(resource, Resource):
            resource = Resource.new_resource_with(resource)

        return resource.get_title()

    def _display(self, callback):
        return self

    def display_using(self, callback):
        return self._display(callback)

    def fill(self, request, model):
        field = model._meta.get_field(self.attribute)

        return super().fill_into(request, model, field.column)

    def fill_attribute_from_request(self, request, request_attribute, model, attribute):
        if request_attribute in request.all():
            value = request.all().get(request_attribute)

            try:
                if self.has_fillable_value(value):
                    setattr(model, attribute, value)
            except:
                pass

    def resolve(self, resource, attribute=None):
        value = getattr(resource, attribute, None)

        if value:
            self.has_one_resource = self.resource_class(value)

            id_for_resource = ID.for_resource(self.resource_class)

            self.has_one_id = (
                id_for_resource
                if id_for_resource
                else Resource.get_key(self.has_one_resource)
            )

            print(self.has_one_id)

            self.value = self.has_one_id

    def build_associatable_query(self, request: DjingRequest):
        queryset = self.resource_class.get_queryset()

        return [item for item in queryset.all()]

    def format_associatable_resource(self, request: DjingRequest, resource: Resource):
        return {
            "display": self._format_display_value(resource),
            "subtitle": resource.subtitle(),
            "value": Resource.get_key(resource),
        }

    def json_serialize(self):
        return array_merge(
            {
                "relationship_type": self.relationship_type(),
                "relationship_name": self.relationship_name(),
                "label": self.resource_class.label(),
                "resource_name": self.resource_name,
                "has_one_id": self.has_one_id,
            },
            super().json_serialize(),
        )

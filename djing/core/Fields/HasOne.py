from typing import Any, Callable, Self
from Illuminate.Support.builtins import array_merge
from Illuminate.Support.Facades.App import App
from djing.core.Contracts.BehavesAsPanel import BehavesAsPanel
from djing.core.Contracts.RelatableField import RelatableField
from djing.core.Fields.Field import Field
from djing.core.Fields.ID import ID
from djing.core.Fields.ResourceRelationshipGuesser import ResourceRelationshipGuesser
from djing.core.Http.Requests.DjingRequest import DjingRequest
from djing.core.Panel import Panel
from djing_admin.app.Djing.Resource import Resource


class HasOne(Field, BehavesAsPanel, RelatableField):
    component = "has-one-field"

    def __init__(self, name, attribute=None, resource=None):
        super().__init__(name, attribute)

        if not attribute:
            raise Exception("Invalid Resource attribute")

        if resource:
            if not issubclass(resource, Resource):
                raise Exception("Invalid Djing Resource")
            else:
                self.resource_class = resource
        else:
            self.resource_class = ResourceRelationshipGuesser.guess_resource(name)

        print(self.resource_class)

        self.resource_name = resource.uri_key()
        self.attribute = attribute
        self.has_one_relationship = attribute
        self.has_one_resource = None
        self.singular_label = name
        self.has_one_id = None
        self._filled_callback: Callable[..., Any] = None

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

    def authorized_to_relate(self, request: DjingRequest):
        resource = request.find_resource_or_fail()

        authorized_to_add = resource.authorized_to_add(
            request, self.resource_class.new_model()
        )

        authorized_to_create = self.resource_class.authorized_to_create(request)

        return authorized_to_add and authorized_to_create

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
            self.already_filled_when(lambda request: True)

            self.has_one_resource = self.resource_class(value)

            id_for_resource = ID.for_resource(self.has_one_resource)

            self.has_one_id = (
                id_for_resource
                if id_for_resource
                else Resource.get_key(self.has_one_resource)
            )

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

    def already_filled_when(self, callback: Callable) -> Self:
        self._filled_callback = callback

        return self

    def already_filled(self, request: DjingRequest):
        return (
            self._filled_callback(request) if callable(self._filled_callback) else False
        )

    def json_serialize(self):
        request: DjingRequest = App.make(DjingRequest)

        return array_merge(
            {
                "relationship_type": self.relationship_type(),
                "relationship_name": self.relationship_name(),
                "label": self.resource_class.label(),
                "resource_name": self.resource_name,
                "relation_id": self.has_one_id,
                "has_one_id": self.has_one_id,
                "relatable": True,
                "already_filled": self.already_filled(request),
                "authorized_to_view": (
                    self.has_one_resource.authorized_to_view(request)
                    if self.has_one_resource
                    else True
                ),
                "authorized_to_create": self.authorized_to_relate(request),
                "create_button_label": self.resource_class.create_button_label(),
                "from": {
                    "via_resource": request.route_param("resource"),
                    "via_resource_id": request.route_param("resource_id"),
                    "via_relationship": self.attribute,
                },
            },
            super().json_serialize(),
        )

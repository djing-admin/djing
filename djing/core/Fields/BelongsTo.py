from Illuminate.Support.builtins import array_merge
from djing.core.Contracts.FilterableField import FilterableField
from djing.core.Contracts.RelatableField import RelatableField
from djing.core.Fields.Field import Field
from djing_admin.app.Djing.Resource import Resource


class BelongsTo(Field, FilterableField, RelatableField):
    component = "belongs-to-field"

    def __init__(self, name, attribute=None, resource=None):
        super().__init__(name, attribute)

        if not resource or not issubclass(resource, Resource):
            raise Exception("Invalid Djing Resource")

        if not attribute:
            raise Exception("Invalid Resource attribute")

        self.resource_class = resource
        self.resource_name = resource.uri_key()
        self.attribute = attribute
        self.belongs_to_relationship = attribute
        self.singular_label = name
        self.belongs_to_id = None

    def relationship_name(self):
        return self.belongs_to_relationship

    def relationship_type(self):
        return "belongs_to"

    def _format_display_value(self, resource):
        if not isinstance(resource, Resource):
            resource = Resource.new_resource_with(resource)

        return resource.get_title()

    def resolve(self, resource, attribute=None):
        super().resolve(resource, attribute)

        value = getattr(resource, attribute)

        if value:
            self.belongs_to_resource = self.resource_class(value)

            self.belongs_to_id = Resource.get_key(self.belongs_to_resource)

            self.value = self._format_display_value(self.belongs_to_resource)

    def json_serialize(self):
        return array_merge(
            {
                "relationship_type": self.relationship_type(),
                "relationship_name": self.relationship_name(),
                "label": self.resource_class.label(),
                "resource_name": self.resource_name,
                "resource_name": self.resource_name,
                "belongs_to_id": self.belongs_to_id,
            },
            super().json_serialize(),
        )

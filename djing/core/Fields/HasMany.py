from typing import Any, Callable, Self
from Illuminate.Support.builtins import array_merge
from djing.core.Contracts.ListableField import ListableField
from djing.core.Contracts.RelatableField import RelatableField
from djing.core.Fields.Collapsable import Collapsable
from djing.core.Fields.Field import Field
from djing.core.Fields.ResourceRelationshipGuesser import ResourceRelationshipGuesser
from djing.core.Http.Requests.DjingRequest import DjingRequest
from djing.core.Panel import Panel
from djing.core.Resource import Resource


class HasMany(Field, ListableField, RelatableField, Collapsable):
    component = "has-many-field"

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

        self.resource_name = self.resource_class.uri_key()
        self.attribute = attribute
        self.has_many_relationship = attribute
        self.has_many_resource = None
        self._singular_label = name
        self._filled_callback: Callable[..., Any] = None

    def singular_label(self, label: str) -> Self:
        self._singular_label = label

        return self

    def as_panel(self):
        return (
            Panel.make(self.name, [self])
            .with_meta({"prefix_component": True})
            .with_component("relationship-panel")
        )

    def relationship_name(self):
        return self.has_many_relationship

    def relationship_type(self):
        return "has_many"

    def authorize(self, request: DjingRequest):
        if hasattr(self.resource_class, "authorized_to_view_any"):
            return super().authorize(request)

    def resolve(self, resource, attribute=None):
        pass

    def help(self, text: str):
        raise Exception("Helper not supported")

    def json_serialize(self):
        return array_merge(
            {
                "collapsable": self._collapsable,
                "collapsed_by_default": self._collapsed_by_default,
                "relationship_type": self.relationship_type(),
                "relationship_name": self.relationship_name(),
                "label": self.resource_class.label(),
                "per_page": self.resource_class._per_page,
                "resource_name": self.resource_name,
                "has_many_relationship": self.has_many_relationship,
                "relatable": True,
                "singular_label": self._singular_label,
            },
            super().json_serialize(),
        )

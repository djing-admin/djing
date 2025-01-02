from typing import TYPE_CHECKING, Self
from Illuminate.Collections.Collection import Collection
from Illuminate.Collections.helpers import collect
from Illuminate.Contracts.Support.JsonSerializable import JsonSerializable
from Illuminate.Support.Str import Str
from Illuminate.Support.builtins import array_merge
from Illuminate.Support.helpers import tap
from djing.core.Fields.Collapsable import Collapsable
from djing.core.Http.Resources.Resource import Resource
from djing.core.Makeable import Makeable
from djing.core.MergeValue import MergeValue
from djing.core.Metable import Metable
from djing.core.Metrics.HasHelpText import HasHelpText
from djing.core.ResourceToolElement import ResourceToolElement

if TYPE_CHECKING:
    from djing.core.Fields.FieldCollection import FieldCollection


class Panel(MergeValue, HasHelpText, Makeable, Metable, Collapsable, JsonSerializable):
    component = "panel"
    _help_text: str = ""
    _limit = None
    _show_toolbar = False

    def __init__(self, name, fields=[], attribute=None):
        self.name = name
        self.attribute = attribute if attribute else Str.slug(name)

        super().__init__(self.prepare_fields(fields))

    @classmethod
    def default_name_for_detail(cls, resource: Resource):
        label = resource.singular_label()

        title = resource.get_title()

        return f"{label} Details: {title}"

    @classmethod
    def default_name_for_update(cls, resource: Resource):
        label = resource.singular_label()

        title = resource.get_title()

        return f"Update {label}: {title}"

    @classmethod
    def default_name_for_create(cls, resource: Resource):
        label = resource.singular_label()

        return f"Create {label}"

    def prepare_fields(self, fields):
        fields = fields() if callable(fields) else fields

        def assign_panel_to_field(field):
            field.assigned_panel = self
            field.panel = self.name

        return (
            collect(fields.all() if isinstance(fields, Collection) else fields)
            .values()
            .each(assign_panel_to_field)
            .all()
        )

    @classmethod
    def mutate(cls, name: str, fields: "FieldCollection"):
        first = fields.first()

        if isinstance(first, ResourceToolElement):
            return (
                cls.make(name)
                .with_component(first.component)
                .with_meta({"fields": fields, "prefix_component": False})
            )

        def map_panel(panel):
            panel.name = name
            panel.with_meta({"fields": fields})

        return tap(first.assigned_panel, map_panel)

    def limit(self, limit) -> Self:
        self._limit = limit

        return self

    def with_toolbar(self) -> Self:
        self._show_toolbar = True

        return self

    def with_component(self, component) -> Self:
        self.component = component

        return self

    def with_attribute(self, attribute) -> Self:
        self.attribute = attribute

        return self

    def json_serialize(self):
        return array_merge(
            {
                "collapsable": self._collapsable,
                "collapsed_by_default": self._collapsed_by_default,
                "name": self.name,
                "component": self.component,
                "attribute": self.attribute,
                "show_toolbar": self._show_toolbar,
                "limit": self._limit,
                "help_text": self.get_help_text(),
            },
            self.meta(),
        )

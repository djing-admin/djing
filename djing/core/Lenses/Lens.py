from abc import abstractmethod
from typing import Any, Optional, Self
from Illuminate.Contracts.Support.JsonSerializable import JsonSerializable
from Illuminate.Support.builtins import array_values
from Illuminate.Support.Str import Str
from django.db.models import Model, QuerySet
from djing.core.AuthorizedToSee import AuthorizedToSee
from djing.core.Facades.Djing import Djing
from djing.core.Fields.FieldCollection import FieldCollection
from djing.core.Fields.ID import ID
from djing.core.Http.Requests.DjingRequest import DjingRequest
from djing.core.Http.Requests.LensRequest import LensRequest
from djing.core.Makeable import Makeable
from djing.core.ResolvesActions import ResolvesActions
from djing.core.ResolvesCards import ResolvesCards
from djing.core.ResolvesFilters import ResolvesFilters


class Lens(
    AuthorizedToSee,
    Makeable,
    ResolvesCards,
    ResolvesFilters,
    ResolvesActions,
    JsonSerializable,
):
    resource: Optional[Model] = None
    _name = ""
    search: list = []

    def __init__(self, resource=None, *args, **kwargs) -> None:
        self.resource = resource if resource else object()

    @classmethod
    @abstractmethod
    def query(cls, request: LensRequest, query: QuerySet):
        raise NotImplementedError("Not Implemented")

    @abstractmethod
    def fields(self, request: DjingRequest):
        raise NotImplementedError("Not Implemented")

    def set_resource(self, resource) -> Self:
        self.resource = resource

        return self

    def name(self) -> str:
        return self._name if self._name else Djing.humanize(self)

    def uri_key(self) -> str:
        return Str.slug(self.name(), "-", None)

    def actions(self, request: DjingRequest) -> Any:
        new_resource = request.new_resource_with(
            self.resource if isinstance(self.resource, Model) else request.model()
        )

        return new_resource.actions(request)

    def resolve_fields(self, request: DjingRequest):
        return (
            self.available_fields(request)
            .filter_for_index(request, self.resource)
            .without_listable_fields()
            .authorized(request)
            .resolve_for_display(self.resource)
        )

    def filterable_fields(self, request: DjingRequest):
        return (
            self.available_fields(request)
            .flatten()
            .with_only_filterable_fields()
            .authorized(request)
        )

    def available_fields(self, request: DjingRequest):
        return FieldCollection(array_values(self.fields(request)))

    @classmethod
    def searchable(cls):
        searchable_columns = cls.searchable_columns()

        return isinstance(searchable_columns, list) and len(searchable_columns) > 0

    @classmethod
    def searchable_columns(cls):
        return cls.search

    def serialize_with_id(self, fields: FieldCollection):
        id_serialize = fields.where_instance_of(ID).first()

        return {
            "id": id_serialize if id_serialize else ID.for_model(self.resource),
            "fields": fields.all(),
        }

    def json_serialize(self):
        return {
            "name": self.name(),
            "uri_key": self.uri_key(),
        }

from abc import ABC
from importlib import import_module
from typing import List, Optional, Self, Type, Union
from Illuminate.Contracts.Support.JsonSerializable import JsonSerializable
from Illuminate.Support.Facades.App import App
from Illuminate.Support.Str import Str
from django.db.models import Model, QuerySet
from django.db.models.base import ModelBase
from djing.core.FillsFields import FillsFields
from djing.core.PerformsValidation import PerformsValidation
from djing.core.ResolvesActions import ResolvesActions
from djing.core.ResolvesLenses import ResolvesLenses
from djing.core.Util import Util
from djing.core.PerformsQueries import PerformsQueries
from djing.core.Authorizable import Authorizable
from djing.core.Fields.Field import Field
from djing.core.Fields.FieldCollection import FieldCollection
from djing.core.Fields.ID import ID
from djing.core.Http.Requests.DjingRequest import DjingRequest
from djing.core.Makeable import Makeable
from djing.core.Menu.MenuItem import MenuItem
from djing.core.ResolvesCards import ResolvesCards
from djing.core.ResolvesFields import ResolvesFields
from djing.core.ResolvesFilters import ResolvesFilters


class Resource(
    ABC,
    Authorizable,
    Makeable,
    PerformsQueries,
    ResolvesCards,
    ResolvesFilters,
    ResolvesFields,
    ResolvesActions,
    ResolvesLenses,
    PerformsValidation,
    FillsFields,
    JsonSerializable,
):
    default_values: dict = {}
    model: Optional[Union[str, Type[Model]]] = None
    resource: Optional[Model] = None
    debounce = 0.5
    searchable = True
    globally_searchable = True
    group = "Other"
    title = ""
    search: list = []
    soft_deletes: list = []
    _per_page_options = [25, 50, 100]
    _per_page = 25
    _available_for_navigation = True

    def __init__(self, resource=None, *args, **kwargs) -> None:
        self.resource = resource

    @classmethod
    def get_model_class(cls) -> Type[Model]:
        if isinstance(cls.model, ModelBase):
            return cls.model

        if isinstance(cls.model, str):
            return cls.get_class_from_string(cls.model)

        raise Exception("Invalid model")

    @classmethod
    def get_queryset(cls) -> QuerySet:
        return cls.get_model_class().objects.get_queryset()

    @classmethod
    def new_model(cls) -> Model:
        model_class = cls.get_model_class()

        return model_class(**cls.default_values)

    def get_model(self) -> Model:
        return self.resource

    @classmethod
    def new_resource(cls) -> "Resource":
        return cls(cls.new_model())

    def get_class_from_string(module_name: str):
        array: List = module_name.split(".")

        name = array.pop()

        class_name = import_module(".".join(array))

        return getattr(class_name, name)

    @classmethod
    def uri_key(cls):
        return Str.plural(Str.kebab(cls.__name__))

    @classmethod
    def label(cls):
        return Str.plural(Str.title(Str.snake(cls.__name__, " ")))

    @classmethod
    def singular_label(cls):
        return Str.singular(cls.label())

    def get_key(self, resource=None):
        resource = resource if resource else self.resource

        pk = Util.get_key_name(resource)

        return getattr(resource, pk)

    def get_title(self):
        pk = Util.get_key_name(self.resource)

        title_attribute = self.title if self.title else pk

        return getattr(self.resource, title_attribute)

    @classmethod
    def is_searchable(cls):
        return cls.searchable and cls.searchable_columns()

    @classmethod
    def searchable_columns(cls):
        pk = Util.get_key_name(cls.new_model())

        return cls.search if cls.search else [pk]

    @classmethod
    def per_page_options(cls):
        return cls._per_page_options

    def menu(self, request: DjingRequest):
        return MenuItem.resource(self.__class__)

    @classmethod
    def available_for_navigation(cls, request: DjingRequest):
        return cls._available_for_navigation

    @classmethod
    def get_soft_deletes(cls) -> bool:
        return True if len(cls.soft_deletes) else False

    def serialize_for_index(self, request: DjingRequest, fields=None):
        id_serialize = self.serialize_with_id(
            fields if fields else self.index_fields(request)
        )

        index_serialize = {
            "title": self.get_title(),
            "actions": self.available_actions_on_table_row(request),
            "authorized_to_view": self.authorized_to_view(request),
            "authorized_to_create": self.authorized_to_create(request),
            "authorized_to_replicate": self.authorized_to_replicate(request),
            "authorized_to_update": self.authorized_to_update(request),
            "authorized_to_delete": self.authorized_to_delete(request),
            "authorized_to_restore": (
                self.get_soft_deletes() and self.authorized_to_restore(request)
            ),
            "authorized_to_force_delete": (
                self.get_soft_deletes() and self.authorized_to_force_delete(request)
            ),
        }

        return {**id_serialize, **index_serialize}

    def serialize_for_detail(self, request: DjingRequest, resource: Self):
        id_serialize = self.serialize_with_id(
            self.detail_fields_within_panels(request, resource)
        )

        detail_serialize = {
            "title": self.get_title(),
            "authorized_to_create": self.authorized_to_create(request),
            "authorized_to_replicate": self.authorized_to_replicate(request),
            "authorized_to_update": self.authorized_to_update(request),
            "authorized_to_delete": self.authorized_to_delete(request),
            "authorized_to_restore": (
                self.get_soft_deletes() and self.authorized_to_restore(request)
            ),
            "authorized_to_force_delete": (
                self.get_soft_deletes() and self.authorized_to_force_delete(request)
            ),
        }

        return {**id_serialize, **detail_serialize}

    def serialize_with_id(self, fields: FieldCollection):
        id_field: Field = fields.where_instance_of(ID).first()

        return {
            "id": id_field if id_field else ID.for_model(self.resource),
            "fields": fields.map(lambda field: field).all(),
        }

    def json_serialize(self):
        return self.serialize_with_id(self.resolve_fields(App.make(DjingRequest)))

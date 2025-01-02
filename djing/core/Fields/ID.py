from typing import Self
from Illuminate.Collections.helpers import data_get
from Illuminate.Support.builtins import array_merge
from django.db.models import base
from djing.core.Fields.Field import Field
from djing.core.Util import Util


class ID(Field):
    component = "id-field"

    @classmethod
    def for_model(cls, resource: base.Model) -> Self:
        key = Util.get_key_name(resource)

        field: Field = cls("ID", key)

        if isinstance(field, int) and data_get(resource, field) >= 9007199254740991:
            field.as_bigint()

        field.resolve(resource)

        return field

    def json_serialize(self):
        return array_merge(super().json_serialize(), {})

from Illuminate.Support.builtins import array_merge
from djing.core.Contracts.ListableField import ListableField
from djing.core.Contracts.RelatableField import RelatableField
from djing.core.Fields.Field import Field


class HasMany(Field, ListableField, RelatableField):
    component = "has-many-field"

    def json_serialize(self):
        return array_merge(
            super().json_serialize(),
            {},
        )

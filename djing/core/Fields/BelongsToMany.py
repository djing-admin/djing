from Illuminate.Support.builtins import array_merge
from djing.core.Contracts.ListableField import ListableField
from djing.core.Contracts.RelatableField import RelatableField
from djing.core.Fields.Field import Field


class BelongsToMany(Field, ListableField, RelatableField):
    component = "belongs-to-many-field"

    def json_serialize(self):
        return array_merge(
            super().json_serialize(),
            {},
        )

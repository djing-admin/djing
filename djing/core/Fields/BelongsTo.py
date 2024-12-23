from Illuminate.Support.builtins import array_merge
from djing.core.Contracts.BehavesAsPanel import BehavesAsPanel
from djing.core.Contracts.RelatableField import RelatableField
from djing.core.Fields.Field import Field


class BelongsTo(Field, BehavesAsPanel, RelatableField):
    component = "belongs-to-field"

    def json_serialize(self):
        return array_merge(
            super().json_serialize(),
            {},
        )

from typing import TYPE_CHECKING, Self
from Illuminate.Support.Facades.App import App
from Illuminate.Collections.helpers import data_get
from Illuminate.Support.builtins import array_merge
from Illuminate.Support.helpers import transform
from django.db.models import base
from djing.core.Fields.Field import Field
from djing.core.Http.Requests.DjingRequest import DjingRequest
from djing.core.Util import Util

if TYPE_CHECKING:
    from djing_admin.app.Djing.Resource import Resource


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

    @classmethod
    def for_resource(cls, resource: "Resource") -> Self | None:
        model = resource.get_model()

        request = App.make(DjingRequest)

        def process_transform(field: Field):
            return field.resolve(model)

        field: Field = transform(
            (
                resource.available_fields_on_index_or_detail(request)
                .where_instance_of(cls)
                .first()
            ),
            process_transform,
        )

        if isinstance(field, Field):
            if not field.value and not field.nullable() != True:
                return None
            else:
                return field

        return None

    def json_serialize(self):
        return array_merge(super().json_serialize(), {})

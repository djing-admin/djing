from typing import Any, Callable, Tuple
from django.db.models import base
from djing.core.Fields.FieldCollection import FieldCollection
from djing.core.Http.Requests.DjingRequest import DjingRequest


class FillsFields:
    @classmethod
    def fill(
        cls, request: DjingRequest, model: base.Model
    ) -> Tuple[base.Model, Callable[..., Any]]:
        return cls._fill_fields(
            request,
            model,
            (
                cls(model)
                .creation_fields(request)
                .without_readonly(request)
                .without_unfillable()
            ),
        )

    @classmethod
    def fill_for_update(cls, request: DjingRequest, model: base.Model):
        return cls._fill_fields(
            request,
            model,
            (
                cls(model)
                .update_fields(request)
                .without_readonly(request)
                .without_unfillable()
            ),
        )

    @classmethod
    def _fill_fields(
        cls, request: DjingRequest, model: base.Model, fields: FieldCollection
    ):
        return [
            model,
            (
                fields.map(lambda field: field.fill(request, model))
                .filter(lambda callback: callable(callback))
                .values()
                .all()
            ),
        ]

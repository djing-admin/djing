from typing import Any
from Illuminate.Helpers.Util import Util
from djing.core.Contracts.Storable import Storable
from djing.core.Http.Requests.DjingRequest import DjingRequest
from django.db.models.base import Model


class DeleteField:
    @classmethod
    def for_request(cls, request: DjingRequest, field: Any, model: Model):
        arguments = [request, model]

        if isinstance(field, Storable):
            arguments.append(field.get_storage_disk())

        results: dict | bool = Util.callback_with_dynamic_args(
            field._delete_callback, arguments
        )

        if isinstance(results, bool):
            return results

        for key, value in results.items():
            setattr(model, key, value)

        model.save()

        return True

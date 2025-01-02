from djing.core.Fields.Filterable import Filterable
from djing.core.Http.Requests.DjingRequest import DjingRequest
from django.db.models import QuerySet


class FieldFilterable(Filterable):
    def _default_filterable_callback(self):
        def filterable_callback(
            request: DjingRequest, query: QuerySet, value, attribute
        ):
            return query.filter(**{attribute: value})

        return filterable_callback

    def _filterable_attribute(self):
        return self.attribute

    def serialize_for_filter(self):
        return self.json_serialize()

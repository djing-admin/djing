from Illuminate.Support.builtins import array_merge
from djing.core.Contracts.FilterableField import FilterableField
from djing.core.Filters.Filter import Filter as BaseFilter
from djing.core.Http.Requests.DjingRequest import DjingRequest
from django.db.models import QuerySet


class Filter(BaseFilter):
    def __init__(self, field: FilterableField):
        self.field = field

    def name(self):
        return self.field.name

    def key(self):
        return f"{self.field.__class__.__name__}:{self.field.attribute}"

    def apply(self, request: DjingRequest, query: QuerySet, value):
        return self.field.apply_filter(request, query, value)

    def serialize_field(self):
        return self.field.serialize_for_filter()

    def json_serialize(self):
        return array_merge(
            super().json_serialize(),
            {
                "component": f"filter-{self.component}",
                "field": self.serialize_field(),
            },
        )

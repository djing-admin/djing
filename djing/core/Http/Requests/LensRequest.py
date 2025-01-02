from typing import Self
from Illuminate.Collections.helpers import collect
from Illuminate.Collections.Collection import Collection
from djing.core.Http.Requests.DecodesFilters import DecodesFilters
from djing.core.Http.Requests.DjingRequest import DjingRequest
from djing.core.Http.Requests.InteractsWithLenses import InteractsWithLenses
from django.db.models import QuerySet

from djing.core.Util import Util


class LensRequest(DecodesFilters, InteractsWithLenses, DjingRequest):
    table_order_prefix = True

    def to_resource(self, models: Collection):
        resource = self.resource()

        def map_models(model):
            lens_resource = self.lens().set_resource(model)

            payload = resource(model).serialize_for_index(
                self, lens_resource.resolve_fields(self)
            )

            payload["actions"] = (
                collect(lens_resource.actions(self))
                .filter(lambda lens_action: lens_action.show_on_index())
                .filter(lambda lens_action: lens_action.authorized_to_see(self))
                .filter(lambda lens_action: lens_action.authorized_to_run(self, model))
                .values()
            )

            return payload

        return models.map(map_models)

    def without_table_prefix(self) -> Self:
        self.table_order_prefix = False

        return self

    def with_filters(self, query: QuerySet):
        return self.filter(query)

    def filter(self, query: QuerySet):
        return self.filters().each(lambda filter: filter(self, query))

    def available_filters(self):
        return self.lens().available_filters(self)

    def per_page(self):
        resource = self.resource()

        per_page_options = resource.per_page_options()

        if not per_page_options:
            per_page_options = [resource._per_page]

        per_page = self.query_param("per_page", resource._per_page)

        return (
            int(per_page) if int(per_page) in per_page_options else per_page_options[0]
        )

    def is_action_request(self):
        return self.segment(5) == "actions"

    def with_orderings(self, query: QuerySet, default_callback=None):
        default_order_by = Util.get_key_name(self.resource().new_model())

        default_order_by_direction = "asc"

        order_by = (
            self.query_param("order_by")
            if self.query_param("order_by")
            else default_order_by
        )

        order_by_direction = (
            self.query_param("order_by_direction")
            if self.query_param("order_by_direction")
            else default_order_by_direction
        )

        field_exists = (
            self.lens()
            .available_fields(self)
            .transform(lambda field: field.attribute)
            .filter()
            .first(lambda attribute: attribute == order_by)
        )

        if field_exists:
            return query.order_by(
                f"-{order_by}" if order_by_direction == "desc" else order_by
            )

        return query

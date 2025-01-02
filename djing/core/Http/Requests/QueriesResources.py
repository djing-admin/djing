from djing.core.Util import Util
from djing.core.Http.Requests.DecodesFilters import DecodesFilters


class QueriesResources(DecodesFilters):
    def new_query(self):
        return self.resource().get_queryset()

    def orderings(self):
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

        return (order_by, order_by_direction)

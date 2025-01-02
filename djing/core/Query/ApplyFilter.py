from django.db.models import QuerySet
from Illuminate.Helpers.Util import Util
from djing.core.Http.Requests.DjingRequest import DjingRequest


class ApplyFilter:
    def __init__(self, filter, value):
        self.filter = filter
        self.value = value

    def __call__(self, request: DjingRequest, query: QuerySet):
        response = Util.callback_with_dynamic_args(
            self.filter.apply, [request, query, self.value]
        )

        return response

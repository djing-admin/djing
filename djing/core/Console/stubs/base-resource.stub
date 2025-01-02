from djing.core.Http.Requests.DjingRequest import DjingRequest
from djing.core.Resource import Resource as DjingResource
from django.db.models import QuerySet


class Resource(DjingResource):
    def index_query(self, request: DjingRequest, query: QuerySet):
        return query

    def detail_query(self, request: DjingRequest, query: QuerySet):
        return super().detail_query(request, query)

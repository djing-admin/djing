from djing.core.Http.Requests.DjingRequest import DjingRequest
from django.db.models import QuerySet


class PerformsQueries:
    def index_query(self, request: DjingRequest, query: QuerySet):
        return query

    def detail_query(self, request: DjingRequest, query: QuerySet):
        return query

    def edit_query(self, request: DjingRequest, query: QuerySet):
        return query

from typing import Tuple
from Illuminate.Support.Facades.App import App
from djing.core.Contracts.QueryBuilder import QueryBuilder
from djing.core.Http.Requests.DjingRequest import DjingRequest
from djing.core.Http.Requests.QueriesResources import QueriesResources
from djing.core.Query.SimplePaginator import SimplePaginator


class ResourceIndexRequest(DjingRequest, QueriesResources):
    request_name = "ResourceIndexRequest"

    def search_index(self) -> Tuple[SimplePaginator, int, bool]:
        qb: QueryBuilder = App.make(
            QueryBuilder, {"app": App.make("app"), "params": [self.resource()]}
        )

        new_query = self.new_query()
        search = self.query_param("search")
        filters = self.filters().all()
        orderings = self.orderings()

        simple_paginator: SimplePaginator = qb.search(
            request=self,
            query=new_query,
            search=search,
            filters=filters,
            orderings=orderings,
        )

        return simple_paginator.paginate(self.per_page())

    def per_page(self) -> int:
        resource = self.resource()

        per_page_options = resource.per_page_options()

        if not per_page_options:
            per_page_options = [resource._per_page]

        per_page = self.query_param("per_page", resource._per_page)

        return (
            int(per_page) if int(per_page) in per_page_options else per_page_options[0]
        )

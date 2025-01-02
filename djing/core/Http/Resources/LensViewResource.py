from Illuminate.Support.Facades.App import App
from djing.core.Contracts.QueryBuilder import QueryBuilder
from djing.core.Http.Requests.LensRequest import LensRequest
from djing.core.Http.Resources.Resource import Resource
from djing.core.Query.SimplePaginator import SimplePaginator


class LensViewResource(Resource):
    def authorized_lens_for_request(self, request: LensRequest):
        return request.lens()

    def json(self, request: LensRequest):
        lens = self.authorized_lens_for_request(request)

        qb: QueryBuilder = App.make(
            QueryBuilder, {"app": App.make("app"), "params": [request.resource()]}
        )

        new_query = request.new_search_query()
        search = request.query_param("search")
        filters = request.with_filters(new_query).all()
        orderings = request.with_orderings(new_query)

        simple_paginator: SimplePaginator = qb.search(
            request=request,
            query=new_query,
            search=search,
            filters=filters,
            orderings=orderings,
        )

        paginator, total, sortable = simple_paginator.paginate(request.per_page())

        resources = request.to_resource(paginator.get_collection())

        return {
            "label": lens.name(),
            "per_page_options": request.resource().per_page_options(),
            "resources": resources,
            "total": total,
            "sortable": sortable,
            "per_page": paginator.per_page(),
            "start_record": paginator.start_record(),
            "end_record": paginator.end_record(),
            "num_pages": paginator.num_pages(),
        }

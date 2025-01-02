from typing import TYPE_CHECKING, Type
from Illuminate.Exceptions.RouteNotFoundException import RouteNotFoundException
from Illuminate.Support.Facades.App import App
from djing.core.Contracts.QueryBuilder import QueryBuilder
from djing.core.Facades.Djing import Djing
from django.db.models import base, QuerySet

if TYPE_CHECKING:
    from djing.core.Resource import Resource


class InteractsWithResources:
    def resource(self) -> Type["Resource"]:
        key = self.route_param("resource")

        resource = Djing.resource_for_key(key)

        if not resource:
            raise RouteNotFoundException(f"The resource {key} could not be found.")

        return resource

    def new_resource(self) -> "Resource":
        resource = self.resource()

        return resource(self.model())

    def new_resource_with(self, model: base.Model) -> "Resource":
        resource = self.resource()

        return resource(model)

    def new_query(self) -> "Resource":
        resource = self.resource()

        return resource.get_queryset()

    def find_resource_or_fail(self, resource_id=None) -> "Resource":
        model: base.Model = self.find_model_or_fail(resource_id)

        return self.new_resource_with(model)

    def find_model_query(self, resource_id=None) -> QuerySet:
        qb: QueryBuilder = App.make(
            QueryBuilder, {"app": App.make("app"), "params": [self.resource()]}
        )

        resource_id = resource_id if resource_id else self.route_param("resource_id")

        return qb.where_key(self.new_query(), resource_id)

    def find_model(self, resource_id=None) -> base.Model:
        query = self.find_model_query(resource_id)

        model = query.first()

        return model

    def find_model_or_fail(self, resource_id=None) -> base.Model:
        model = self.find_model(resource_id)

        if not model:
            raise RouteNotFoundException("Resource not found")

        return model

    def model(self) -> base.Model:
        resource = self.resource()

        return resource.new_model()

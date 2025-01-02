from Illuminate.Exceptions.RouteNotFoundException import RouteNotFoundException
from Illuminate.Exceptions.UnauthorizedAccessException import (
    UnauthorizedAccessException,
)
from djing.core.Http.Requests.DjingRequest import DjingRequest
from djing.core.Http.Requests.QueriesResources import QueriesResources
from djing.core.Metrics.Metric import Metric
from djing.core.Resource import Resource


class MetricRequest(DjingRequest, QueriesResources):
    request_name = "MetricRequest"

    def metric(self):
        metric = self.available_metrics().first(
            lambda metric: metric.uri_key() == self.route_param("metric")
        )

        if not metric:
            raise RouteNotFoundException("Metric not found")

        return metric

    def detail_metric(self):
        metric = self.available_metrics_for_detail().first(
            lambda metric: metric.uri_key() == self.route_param("metric")
        )

        if not metric:
            raise RouteNotFoundException("Metric not found")

        return metric

    def available_metrics(self):
        resource: Resource = self.new_resource()

        if not resource.authorized_to_view_any(self):
            raise UnauthorizedAccessException(
                "Unauthorized: MetricRequest.available_metrics"
            )

        return resource.available_cards(self).where_instance_of(Metric)

    def available_metrics_for_detail(self):
        resource: Resource = self.new_resource()

        if not resource.authorized_to_view_any(self):
            raise UnauthorizedAccessException(
                "Unauthorized: MetricRequest.available_metrics_for_detail"
            )

        return resource.available_cards_for_detail(self).where_instance_of(Metric)

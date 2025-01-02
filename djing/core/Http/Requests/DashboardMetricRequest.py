from Illuminate.Exceptions.RouteNotFoundException import RouteNotFoundException
from djing.core.Foundation.Djing import Djing
from djing.core.Http.Requests.DjingRequest import DjingRequest
from djing.core.Http.Requests.QueriesResources import QueriesResources
from djing.core.Metrics.Metric import Metric


class DashboardMetricRequest(DjingRequest, QueriesResources):
    request_name = "DashboardMetricRequest"

    def metric(self):
        metric = self.available_metrics().first(
            lambda metric: metric.uri_key() == self.route_param("metric")
        )

        if not metric:
            raise RouteNotFoundException("Metric not found")

        return metric

    def available_metrics(self):
        return Djing.all_available_dashboard_cards(self).where_instance_of(Metric)

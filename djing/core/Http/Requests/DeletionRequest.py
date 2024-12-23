from typing import Type
from Illuminate.Collections.helpers import collect
from djing.core.Http.Requests.DjingRequest import DjingRequest
from djing.core.Http.Requests.QueriesResources import QueriesResources
from djing.core.Resource import Resource


class DeletionRequest(QueriesResources, DjingRequest):
    def chunk_with_authorization(self, count, callback, auth_callback):
        queryset = self.to_selected_resource_query()

        auth_callback_response = auth_callback(collect(list(queryset.all())))

        return callback(auth_callback_response)

    def to_selected_resource_query(self):
        if self.all_resources_selected():
            return self.new_query()
        else:
            resource: Type[Resource] = self.resource()

            return resource.get_queryset().filter(id__in=self.selected_resource_ids())

from typing import Type
from Illuminate.Collections.Collection import Collection
from djing.core.Http.Requests.DjingRequest import DjingRequest
from djing.core.Makeable import Makeable
from djing.core.Resource import Resource


class ResourceCollection(Collection[Type[Resource]], Makeable):
    def authorized(self, request: DjingRequest):
        return self.filter(lambda resource: resource.authorized_to_view_any(request))

    def searchable(self):
        return self.filter(lambda resource: resource.globally_searchable)

    def grouped(self):
        return self.group_by(lambda resource, key: resource.group).to_base().sort_keys()

    def available_for_navigation(self, request: DjingRequest):
        return self.filter(lambda resource: resource.available_for_navigation(request))

    def grouped_for_navigation(self, request: DjingRequest):
        return self.available_for_navigation(request).grouped()

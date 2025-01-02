from typing import Any
from django.db.models import base


class InteractsWithResourcesSelection:
    def all_resources_selected(self) -> bool:
        resources = self.query_param("resources")

        return resources == "all"

    def selected_resource_ids(self) -> Any:
        if self.all_resources_selected():
            return None

        resources = self.query_param("resources")

        if resources:
            return [int(id) for id in resources.split(",")]

        if isinstance(self.resource, base.Model):
            return [self.get_key()]

        return []

from djing.core.Facades.Djing import Djing


class InteractsWithRelatedResources:
    def via_relationship(self) -> bool:
        return self.query_param("via_resource") and self.query_param("via_resource_id")

    def via_resource(self):
        resource_key = self.query_param("via_resource")

        return Djing.resource_for_key(resource_key)

    def new_resource_via(self):
        resource = self.via_resource()

        return resource(resource.new_model())

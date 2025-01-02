from Illuminate.Collections.Collection import Collection
from djing.core.Http.Requests.DeletionRequest import DeletionRequest


class DeleteResourceRequest(DeletionRequest):
    def chunks(self, count, callback):
        return self.chunk_with_authorization(
            count, callback, lambda models: self.deletable_models(models)
        )

    def deletable_models(self, models: Collection):
        return (
            models.map_into(self.resource())
            .filter(lambda model: model.authorized_to_delete(self))
            .map(lambda model: model.resource)
        )

    def is_for_single_resource(self) -> bool:
        resources = self.query_param("resources")

        return resources != "all" and len(resources) == 1

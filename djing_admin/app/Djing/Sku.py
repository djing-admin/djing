from djing.core.Fields.BelongsTo import BelongsTo
from djing.core.Fields.ID import ID
from djing.core.Fields.Text import Text
from djing.core.Http.Requests.DjingRequest import DjingRequest
from djing_admin.app.Djing.Resource import Resource as DjingResource


class Sku(DjingResource):
    model = "skus.models.Sku"
    title = "name"
    search = [
        "id",
    ]

    def fields(self, request: DjingRequest):
        from djing_admin.app.Djing.Product import Product

        return [
            ID.make("ID").sortable(),
            Text.make("Name"),
            BelongsTo.make("Product", "product", Product),
        ]

    def cards(self, request: DjingRequest):
        return []

    def filters(self, request: DjingRequest):
        return []

    def lenses(self, request: DjingRequest):
        return []

    def actions(self, request: DjingRequest):
        return []

from djing.core.Fields.HasOne import HasOne
from djing.core.Fields.Image import Image
from djing.core.Fields.Currency import Currency
from djing.core.Fields.BelongsTo import BelongsTo
from djing.core.Fields.ID import ID
from djing.core.Fields.Text import Text
from djing.core.Http.Requests.DjingRequest import DjingRequest
from djing_admin.app.Djing.Resource import Resource as DjingResource


class Product(DjingResource):
    model = "products.models.Product"
    title = "name"
    search = [
        "id",
    ]

    def fields(self, request: DjingRequest):
        from djing_admin.app.Djing.Sku import Sku
        from djing_admin.app.Djing.User import User

        return [
            ID.make("ID").sortable(),
            Text.make("Name"),
            Image.make("Image"),
            Currency.make("Price"),
            HasOne.make("Sku", "sku", Sku),
            BelongsTo.make("User", "user", User),
        ]

    def cards(self, request: DjingRequest):
        return []

    def filters(self, request: DjingRequest):
        return []

    def lenses(self, request: DjingRequest):
        return []

    def actions(self, request: DjingRequest):
        return []

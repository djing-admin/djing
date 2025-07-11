from djing.core.Fields.Boolean import Boolean
from djing.core.Fields.Email import Email
from djing.core.Fields.Gravatar import Gravatar
from djing.core.Fields.HasMany import HasMany
from djing.core.Fields.ID import ID
from djing.core.Fields.Password import Password
from djing.core.Fields.Text import Text
from djing.core.Http.Requests.DjingRequest import DjingRequest
from django.contrib.auth import get_user_model
from djing.core.Rules.Unique import Unique
from djing_admin.app.Djing.Resource import Resource as DjingResource

UserModel = get_user_model()


class User(DjingResource):
    model = UserModel
    title = "username"
    search = [
        "id",
        "first_name",
        "last_name",
        "username",
        "email",
    ]

    def fields(self, request: DjingRequest):
        from djing_admin.app.Djing.Product import Product

        return [
            ID.make("ID").sortable(),
            Gravatar.make("Avatar"),
            (
                Text.make("Username")
                .sortable()
                .required()
                .rules("required", "max:255")
                .placeholder("Write your Username")
            ),
            (
                Email.make("Email Address", "email")
                .sortable()
                .required()
                .rules("required", "email", "max:255")
                .creation_rules([Unique(UserModel, "email")])
                .update_rules(
                    [Unique(UserModel, "email", request.route_param("resource_id"))]
                )
                .placeholder("Write your Email Address")
            ),
            (
                Password.make("Password")
                .only_on_forms()
                .creation_rules("required", "min:8")
                .update_rules("nullable", "min:8")
            ),
            Boolean.make("Super User", "is_superuser").sortable(),
            Boolean.make("Staff", "is_staff").sortable(),
            Boolean.make("Active", "is_active").sortable(),
            HasMany.make("Products", "products", Product),
        ]

    def cards(self, request: DjingRequest):
        return []

    def filters(self, request: DjingRequest):
        return []

    def lenses(self, request: DjingRequest):
        return []

    def actions(self, request: DjingRequest):
        return []

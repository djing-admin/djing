from Illuminate.Validation.Rule import Rule


class Exists(Rule):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def validate(self) -> bool:
        self.require_params_count(2)

        UserModel = self.args.get(0)

        username_field = self.args.get(1)

        credentials = {username_field: self.params.get("value")}

        user = UserModel.objects.filter(**credentials).first()

        return user is not None

    def get_message(self) -> str:
        return "User does not exists"

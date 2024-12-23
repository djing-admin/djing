from Illuminate.Validation.Rule import Rule


class Unique(Rule):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def validate(self) -> bool:
        self.require_params_count(2)

        UserModel = self.args.get(0)

        username_field = self.args.get(1)

        id = self.args.get(2)

        credentials = {username_field: self.params.get("value")}

        user = UserModel.objects.filter(**credentials).first()

        if id:
            if user:
                return int(id) == int(user.id)
            else:
                return True

        return user is None

    def get_message(self) -> str:
        return "The Email has already been taken."

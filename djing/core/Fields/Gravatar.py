import hashlib
from Illuminate.Support.builtins import array_merge
from djing.core.Fields.Avatar import Avatar
from djing.core.Fields.Unfillable import Unfillable


class Gravatar(Avatar, Unfillable):
    _max_width = 50

    def __init__(self, name="Avatar", attribute="email"):
        super().__init__(name, attribute if attribute else "email")

        self.except_on_forms()

    def _resolve_attribute(self, resource, attribute):
        value = super()._resolve_attribute(resource, attribute)

        def gravatar_callback(value):
            if value is not None:
                value = str(value).lower()

                value = value.encode("utf-8")

                value = hashlib.md5(value).hexdigest()

                return f"https://www.gravatar.com/avatar/{value}?s=300"

            return None

        self.preview(lambda: gravatar_callback(value)).thumbnail(
            lambda: gravatar_callback(value)
        )

    def json_serialize(self):
        return array_merge(
            {
                "index_name": "",
            },
            super().json_serialize(),
        )

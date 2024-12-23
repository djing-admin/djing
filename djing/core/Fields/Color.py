from djing.core.Fields.Field import Field


class Color(Field):
    component = "color-field"

    def json_serialize(self):
        return super().json_serialize()

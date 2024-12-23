from djing.core.Fields.Text import Text


class Hidden(Text):
    component = "hidden-field"

    def __init__(self, name, attribute=None, resolve_callback=None):
        super().__init__(name, attribute, resolve_callback)

        self.only_on_forms()

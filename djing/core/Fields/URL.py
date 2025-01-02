from djing.core.Fields.Text import Text


class URL(Text):
    component = "url-field"

    def __init__(self, name, attribute=None, resolve_callback=None):
        super().__init__(name, attribute, resolve_callback)

        self.text_align(self.CENTER_ALIGN)

    def resolve(self, resource, attribute=None):
        self._displayed_as = self.name

        super().resolve(resource, attribute)

    def copyable(self):
        raise Exception("Helper not supported")

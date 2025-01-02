from djing.core.Fields.Image import Image


class Avatar(Image):
    def __init__(self, name, attribute=None, disk=None, storage_callback=None):
        super().__init__(name, attribute, disk, storage_callback)

        self.rounded()

    @classmethod
    def gravatar(cls, name="Avatar", attribute="email"):
        from djing.core.Fields.Gravatar import Gravatar

        return Gravatar(name, attribute)

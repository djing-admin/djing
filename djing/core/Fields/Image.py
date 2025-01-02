from Illuminate.Support.builtins import array_merge
from djing.core.Fields.File import File
from djing.core.Fields.PresentsImages import PresentsImages


class Image(File, PresentsImages):
    _show_on_index = True

    ASPECT_AUTO = "aspect-auto"
    ASPECT_SQUARE = "aspect-square"

    def __init__(self, name, attribute=None, disk=None, storage_callback=None):
        super().__init__(name, attribute, disk, storage_callback)

        self.accepted_types("image/*")

        self.thumbnail(self._default_thumbnail_callback).preview(
            self._default_preview_callback
        )

    def _default_thumbnail_callback(self):
        storage_disk = self.get_storage_disk()

        return storage_disk.url(str(self.value)) if self.value else None

    def _default_preview_callback(self):
        storage_disk = self.get_storage_disk()

        return storage_disk.url(str(self.value)) if self.value else None

    def json_serialize(self):
        return array_merge(super().json_serialize(), self.image_attributes())

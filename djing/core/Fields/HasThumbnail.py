from typing import Any, Callable, Self
from Illuminate.Helpers.Util import Util


class HasThumbnail:
    _thumbnail_url_callback: Callable[..., Any]

    def thumbnail(self, thumbnail_url_callback) -> Self:
        self._thumbnail_url_callback = thumbnail_url_callback

        return self

    def resolve_thumbnail_url(self):
        if callable(self._thumbnail_url_callback):
            value = str(self.value) if self.value is not None else None

            return Util.callback_with_dynamic_args(
                self._thumbnail_url_callback,
                [value, self.get_storage_disk(), self.resource],
            )

        return None

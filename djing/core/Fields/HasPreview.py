from typing import Any, Callable, Self
from Illuminate.Helpers.Util import Util


class HasPreview:
    _preview_url_callback: Callable[..., Any]

    def preview(self, preview_url_callback) -> Self:
        self._preview_url_callback = preview_url_callback

        return self

    def resolve_preview_url(self):
        if callable(self._preview_url_callback):
            value = str(self.value) if self.value is not None else None

            return Util.callback_with_dynamic_args(
                self._preview_url_callback,
                [value, self.get_storage_disk(), self.resource],
            )

        return None

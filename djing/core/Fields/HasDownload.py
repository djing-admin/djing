from typing import Any, Self, Callable

from Illuminate.Helpers.Util import Util
from djing.core.Http.Requests.DjingRequest import DjingRequest
from djing.core.Resource import Resource


class HasDownload:
    _downloads_are_enabled = True
    _download_response_callback: Callable[..., Any]

    def disable_downloads(self) -> Self:
        self._downloads_are_enabled = False

        return self

    def download(self, download_response_callback) -> Self:
        self._download_response_callback = download_response_callback

        return self

    def to_download_response(self, request: DjingRequest, resource: Resource):
        return Util.callback_with_dynamic_args(
            self._download_response_callback,
            [request, resource, self.get_storage_disk()],
        )

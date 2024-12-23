import os

from typing import Any, Callable, Self
from Illuminate.Helpers.Util import Util
from Illuminate.Support.Str import Str
from Illuminate.Support.builtins import array_merge
from djing.core.Contracts.Downloadable import Downloadable as DownloadableContract
from djing.core.Contracts.Deletable import Deletable as DeletableContract
from djing.core.Contracts.Storable import Storable as StorableContract
from djing.core.Fields.Storable import Storable
from djing.core.Fields.AcceptsTypes import AcceptsTypes
from djing.core.Fields.Deletable import Deletable
from djing.core.Fields.Field import Field
from djing.core.Fields.HasDownload import HasDownload
from djing.core.Fields.HasPreview import HasPreview
from djing.core.Fields.HasThumbnail import HasThumbnail
from djing.core.Http.Requests.DjingRequest import DjingRequest
from django.core.files.storage import Storage
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile


class File(
    Field,
    Storable,
    Deletable,
    HasDownload,
    HasThumbnail,
    HasPreview,
    AcceptsTypes,
    DeletableContract,
    DownloadableContract,
    StorableContract,
):
    component = "file-field"

    _text_align = "center"
    _show_on_index = False

    _storage_callback: Callable[..., dict]
    _store_as_callback: Callable[..., str] | None = None
    _original_name_column = None
    _size_column = None

    def __init__(self, name, attribute=None, disk=None, storage_callback=None):
        super().__init__(name, attribute)

        self.disk(disk)

        storage_callback = (
            storage_callback if storage_callback else self._default_storage_callback
        )

        (
            self.store(storage_callback)
            .thumbnail(self._default_thumbnail_callback)
            .preview(self._default_preview_callback)
            .download(self._default_download_response_callback)
            .delete(self._default_delete_callback)
        )

    def _default_thumbnail_callback(self):
        return None

    def _default_preview_callback(self):
        return None

    def _default_download_response_callback(self):
        storage_disk = self.get_storage_disk()

        download_url = storage_disk.path(str(self.value))

        return download_url

    def _default_delete_callback(self):
        if self.value is not None:
            storage_disk = self.get_storage_disk()

            storage_disk.delete(str(self.value))

            return {
                self.attribute: None,
            }

    def get_storage_disk(self) -> Storage:
        return self._disk if self._disk else default_storage

    def store(self, storage_callback) -> Self:
        self._storage_callback = storage_callback

        return self

    def store_as(self, store_as_callback) -> Self:
        self._store_as_callback = store_as_callback

        return self

    def store_original_name(self, original_name_column) -> Self:
        self._original_name_column = original_name_column

        return self

    def store_size(self, size_column) -> Self:
        self._size_column = size_column

        return self

    def get_storage_callback(self) -> Storage:
        return self._disk if self._disk else default_storage

    def _default_store_as_callback(
        self, request: DjingRequest, request_attribute
    ) -> str:
        file = self._retrieve_file_from_request(request, request_attribute)

        random_string = Str.random()

        file_extension: str = os.path.splitext(file.name)[1].lstrip(".")

        return f"{random_string}.{file_extension}"

    def _retrieve_file_from_request(self, request: DjingRequest, request_attribute):
        data = request.all()

        return data.get(request_attribute)

    def _merge_extra_storage_columns(
        self, request: DjingRequest, request_attribute, attributes
    ) -> dict:
        file = self._retrieve_file_from_request(request, request_attribute)

        if self._original_name_column:
            attributes[self._original_name_column] = file.name

        if self._size_column:
            attributes[self._size_column] = file.size

        return attributes

    def _store_file(self, request: DjingRequest, request_attribute):
        file: Any = self._retrieve_file_from_request(request, request_attribute)

        storage = self.get_storage_disk()

        file_name = (
            Util.callback_with_dynamic_args(
                self._store_as_callback, [request, request_attribute]
            )
            if self._store_as_callback
            else self._default_store_as_callback(request, request_attribute)
        )

        storage_dir = self.get_storage_dir()

        file_name = (
            f"{storage_dir.rstrip('/')}/{file_name}" if storage_dir else file_name
        )

        response = storage.save(file_name, ContentFile(file.read()))

        return response

    def _default_storage_callback(
        self, request: DjingRequest, request_attribute, model, attribute
    ) -> dict:
        return self._merge_extra_storage_columns(
            request,
            request_attribute,
            {
                self.attribute: self._store_file(request, request_attribute),
            },
        )

    def resolve_default_value(self, request: DjingRequest):
        return str(self.value) if self.value is not None else None

    def fill_for_action(self, request: DjingRequest, model):
        value = request.route_param(self.attribute)

        if self.has_fillable_value(value):
            setattr(model, self.attribute, value)

    def fill_attribute(
        self, request: DjingRequest, request_attribute, model, attribute
    ):
        file: Any = self._retrieve_file_from_request(request, request_attribute)

        if not file:
            return

        results: dict = Util.callback_with_dynamic_args(
            self._storage_callback,
            [request, request_attribute, model, attribute],
        )

        if not isinstance(results, dict):
            return

        for key, value in results.items():
            if self.has_fillable_value(value):
                setattr(model, key, value)

    def json_serialize(self):
        return array_merge(
            super().json_serialize(),
            {
                "thumbnail_url": self.resolve_thumbnail_url(),
                "preview_url": self.resolve_preview_url(),
                "downloadable": self.value is not None and self._downloads_are_enabled,
                "deletable": callable(self._delete_callback) and self._deletable,
                "accepted_types": self._accepted_types,
            },
        )

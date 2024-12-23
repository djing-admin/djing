from typing import Self
from django.core.files.storage import Storage


class Storable:
    _disk = None
    _storage_path: str | None = None

    def disk(self, storage_disk) -> Self:
        if storage_disk is not None and not isinstance(storage_disk, Storage):
            raise Exception("Invalid Storage Disk")

        self._disk = storage_disk

        return self

    def path(self, storage_path) -> Self:
        self._storage_path = storage_path

        return self

    def get_storage_dir(self) -> str | None:
        return self._storage_path

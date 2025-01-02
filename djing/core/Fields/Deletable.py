from typing import Self


class Deletable:
    _delete_callback = None
    _deletable = True

    def delete(self, callback) -> Self:
        self._delete_callback = callback

        return self

    def deletable(self, deletable=True) -> Self:
        self._deletable = deletable

        return self

from typing import Self


class SupportsFullWidth:
    _full_width = False

    def full_width(self) -> Self:
        self._full_width = True

        return self

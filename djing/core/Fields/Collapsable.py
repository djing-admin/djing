from typing import Self


class Collapsable:
    _collapsable = False
    _collapsed_by_default = False

    def collapsable(self) -> Self:
        self._collapsable = True

        return self

    def collapsible(self) -> Self:
        return self.collapsable()

    def collapsed_by_default(self) -> Self:
        self.collapsable()
        self._collapsed_by_default = True

        return self

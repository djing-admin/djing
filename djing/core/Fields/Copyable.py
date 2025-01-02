from typing import Self


class Copyable:
    _as_html = False
    _copyable = False

    def copyable(self) -> Self:
        if self._as_html:
            raise Exception("Please remove as_html to support copyable")

        self._copyable = True

        return self

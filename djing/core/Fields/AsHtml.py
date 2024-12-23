from typing import Self


class AsHtml:
    _as_html = False
    _copyable = False

    def as_html(self) -> Self:
        if self._copyable:
            raise Exception("Please remove copyable to support as_html")

        self._as_html = True

        return self

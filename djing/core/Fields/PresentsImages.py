from typing import Self


class PresentsImages:
    _max_width = None
    _index_width = 32
    _detail_width = 128
    _rounded = False
    _aspect = "aspect-auto"

    def max_width(self, max_width) -> Self:
        self._max_width = max_width

        return self

    def index_width(self, index_width) -> Self:
        self._index_width = index_width

        return self

    def detail_width(self, detail_width) -> Self:
        self._detail_width = detail_width

        return self

    def aspect(self, aspect) -> Self:
        self._aspect = aspect

        return self

    def rounded(self) -> Self:
        self._rounded = True

        return self

    def squared(self) -> Self:
        self._rounded = False

        return self

    def is_rounded(self) -> bool:
        return self._rounded == True

    def is_squared(self) -> bool:
        return self._rounded == False

    def image_attributes(self):
        return {
            "index_width": self._index_width,
            "detail_width": self._detail_width,
            "max_width": self._max_width,
            "aspect": self._aspect,
            "rounded": self.is_rounded(),
        }

from Illuminate.Support.builtins import array_merge
from djing.core.Element import Element


class Card(Element):
    FULL_WIDTH = "full"
    ONE_THIRD_WIDTH = "1/3"
    ONE_HALF_WIDTH = "1/2"
    ONE_QUARTER_WIDTH = "1/4"
    TWO_THIRDS_WIDTH = "2/3"
    THREE_QUARTERS_WIDTH = "3/4"
    FIXED_HEIGHT = "fixed"
    DYNAMIC_HEIGHT = "dynamic"

    _width = ONE_THIRD_WIDTH
    _height = FIXED_HEIGHT

    def width(self, width):
        self._width = width

        if self._width == self.FULL_WIDTH:
            self._height = self.DYNAMIC_HEIGHT

        return self

    def hight(self, height):
        self._height = height

        return self

    def dynamic_hight(self):
        self._height = self.DYNAMIC_HEIGHT

        return self

    def fixed_hight(self):
        self._height = self.FIXED_HEIGHT

        return self

    def json_serialize(self) -> dict:
        return array_merge(
            {
                "width": self._width,
                "height": self._height,
            },
            super().json_serialize(),
        )

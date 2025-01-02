from typing import Self
from Illuminate.Support.Str import Str
from djing.core.Element import Element
from djing.core.Panel import Panel
from djing.core.ResourceToolElement import ResourceToolElement


class ResourceTool(Panel):
    _name = None
    _tool_component = None

    def __init__(self):
        super().__init__(self.name(), [ResourceToolElement(self.tool_component())])

        self.element: Element = self.data[0]

    def name(self):
        return (
            self._name
            if self._name
            else Str.title(Str.snake(self.__class__.__name__, " "))
        )

    def tool_component(self):
        return (
            self._tool_component
            if self._tool_component
            else Str.kebab(self.__class__.__name__, " ")
        )

    def can_see(self, callback) -> Self:
        self.element.can_see(callback)

        return self

    def with_meta(self, meta) -> Self:
        self.element.with_meta(meta)

        return self

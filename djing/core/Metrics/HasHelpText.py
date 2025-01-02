from typing import Self


class HasHelpText:
    _help_text: str = ""
    _help_width: str | int = 250

    def help(self, help_text: str) -> Self:
        self._help_text = help_text

        return self

    def get_help_text(self) -> str:
        return self._help_text

    def help_width(self, help_width: str | int) -> Self:
        self._help_width = help_width

        return self

    def get_help_width(self) -> str | int:
        return self._help_width

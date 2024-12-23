from typing import Self

from Illuminate.Contracts.Support.JsonSerializable import JsonSerializable


class ValueResult(JsonSerializable):
    def __init__(self, value):
        self._value = value
        self._previous = None
        self._previous_label = None
        self._copyable = False
        self._format = "(0[.]00a)"
        self._tooltip_format = "(0[.]00a)"
        self._prefix = None
        self._suffix = None
        self._suffix_inflection = True
        self._zero_result = False

    def previous(self, results, previous_label=None) -> Self:
        self._previous = results
        self._previous_label = previous_label

        return self

    def dollars(self, symbol="$") -> Self:
        return self.currency(symbol)

    def currency(self, symbol="$") -> Self:
        return self.prefix(symbol)

    def prefix(self, prefix: str) -> Self:
        self._prefix = prefix

        return self

    def suffix(self, suffix: str) -> Self:
        self._suffix = suffix

        return self

    def without_suffix_inflection(self) -> Self:
        self._suffix_inflection = False

        return self

    def format(self, format: str) -> Self:
        self._format = format

        return self

    def tooltip_format(self, tooltip_format: str) -> Self:
        self._tooltip_format = tooltip_format

        return self

    def allow_zero_result(self, zero_result=True) -> Self:
        self._zero_result = zero_result

        return self

    def copyable(self) -> Self:
        self._copyable = True

        return self

    def json_serialize(self):
        return {
            "value": self._value,
            "previous": self._previous,
            "previous_label": self._previous_label,
            "copyable": self._copyable,
            "format": self._format,
            "tooltip_format": self._tooltip_format,
            "prefix": self._prefix,
            "suffix": self._suffix,
            "suffix_inflection": self._suffix_inflection,
            "zero_result": self._zero_result,
        }

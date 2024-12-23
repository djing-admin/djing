from typing import Self

from Illuminate.Contracts.Support.JsonSerializable import JsonSerializable


class ProgressResult(JsonSerializable):
    def __init__(self, value, target):
        self._value = value
        self._target = target
        self._avoid = False
        self._format = "(0[.]00a)"
        self._tooltip_format = "(0[.]00a)"
        self._prefix = None
        self._suffix = None
        self._suffix_inflection = True

    def avoid(self, avoid=True) -> Self:
        self._avoid = avoid

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

    def get_percentage(self):
        return round((float(self._value) / float(self._target)) * 100, 2)

    def json_serialize(self):
        return {
            "value": self._value,
            "target": self._target,
            "percentage": self.get_percentage(),
            "avoid": self._avoid,
            "format": self._format,
            "tooltip_format": self._tooltip_format,
            "prefix": self._prefix,
            "suffix": self._suffix,
            "suffix_inflection": self._suffix_inflection,
        }

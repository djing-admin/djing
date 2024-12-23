from typing import Any, Dict, Self
from Illuminate.Support.builtins import array_merge_recursive
from djing.core.Http.Requests.DjingRequest import DjingRequest


class HandlesValidation:
    _rules: list = []
    _creation_rules: list = []
    _update_rules: list = []

    def get_creation_rules(self, request: DjingRequest) -> Dict[Any, Any]:
        key = self.validation_key()

        rules = {
            key: (
                self._creation_rules(request)
                if callable(self._creation_rules)
                else self._creation_rules
            ),
        }

        merged_rules = array_merge_recursive(self.get_rules(request), rules)

        return merged_rules

    def get_update_rules(self, request: DjingRequest) -> Dict[Any, Any]:
        key = self.validation_key()

        rules = {
            key: (
                self._update_rules(request)
                if callable(self._update_rules)
                else self._update_rules
            ),
        }

        merged_rules = array_merge_recursive(self.get_rules(request), rules)

        return merged_rules

    def get_rules(self, request: DjingRequest) -> Dict[Any, Any]:
        key = self.validation_key()

        return {key: (self._rules(request) if callable(self._rules) else self._rules)}

    def rules(self, *rules) -> Self:
        self._rules = self._parse_rules(rules)

        return self

    def creation_rules(self, *rules) -> Self:
        self._creation_rules = self._parse_rules(rules)

        return self

    def update_rules(self, *rules) -> Self:
        self._update_rules = self._parse_rules(rules)

        return self

    def _parse_rules(self, rules):
        rules = list(rules)

        if len(rules) > 1:
            return rules

        if isinstance(rules[0], list):
            return rules[0]

        return rules

    def validation_key(self) -> str:
        return self.attribute

from typing import Any, Dict


class Metable:
    _meta: Dict[Any, Any] = {}

    def meta(self):
        return self._meta

    def with_meta(self, meta):
        self._meta = {**self._meta, **meta}

        return self

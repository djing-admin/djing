from typing import Self


class AcceptsTypes:
    _accepted_types = None

    def accepted_types(self, accepted_types) -> Self:
        self._accepted_types = accepted_types

        return self

from typing import Any, Callable, Self
from Illuminate.Support.Facades.App import App
from Illuminate.Support.builtins import array_merge
from djing.core.Fields.Field import Field
from djing.core.Http.Requests.DjingRequest import DjingRequest


class KeyValue(Field):
    component = "key-value-field"

    _show_on_index = False
    _key_label = "Key"
    _value_label = "Value"
    _action_text = "Add Row"
    _readonly_keys_callback: Callable[..., Any] | bool = False
    _can_add_row = True
    _can_delete_row = True

    def resolve(self, resource, attribute=None):
        super().resolve(resource, attribute)

        if self.value == "{}":
            self.value = None

    def key_label(self, label) -> Self:
        self._key_label = label

        return self

    def value_label(self, label) -> Self:
        self._value_label = label

        return self

    def action_text(self, label) -> Self:
        self._action_text = label

        return self

    def disable_editing_keys(self, callback=True) -> Self:
        self._readonly_keys_callback = callback

        return self

    def readonly_keys(self, request: DjingRequest) -> bool:
        if callable(self._readonly_keys_callback):
            return self._readonly_keys_callback(request)

        return self._readonly_keys_callback == True

    def disable_adding_rows(self) -> Self:
        self._can_add_row = False

        return self

    def disable_deleting_rows(self) -> Self:
        self._can_delete_row = False

        return self

    def json_serialize(self):
        return array_merge(
            super().json_serialize(),
            {
                "key_label": self._key_label,
                "value_label": self._value_label,
                "action_text": self._action_text,
                "readonly_keys": self.readonly_keys(App.make(DjingRequest)),
                "can_add_row": self._can_add_row,
                "can_delete_row": self._can_delete_row,
            },
        )

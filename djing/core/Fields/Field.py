from typing import Any, Self
from Illuminate.Contracts.Support.JsonSerializable import JsonSerializable
from Illuminate.Contracts.Resolvable import Resolvable
from Illuminate.Helpers.Util import Util
from Illuminate.Support.Facades.App import App
from Illuminate.Support.Str import Str
from Illuminate.Collections.helpers import data_get, value
from djing.core.Fields.FieldElement import FieldElement
from djing.core.Fields.HandlesValidation import HandlesValidation
from djing.core.Fields.SupportsFullWidth import SupportsFullWidth
from djing.core.Http.Requests.DjingRequest import DjingRequest
from django.db.models.query_utils import DeferredAttribute

from djing.core.Metrics.HasHelpText import HasHelpText


class Field(
    FieldElement,
    HasHelpText,
    SupportsFullWidth,
    HandlesValidation,
    JsonSerializable,
    Resolvable,
):
    _is_bigint = True
    _sortable = False
    _nullable = False
    _placeholder = None
    _visible = True
    _with_label = True
    _help_text = ""
    _text_align = "left"
    _inline = False

    _displayed_as = None
    _uses_customized_display = False

    _resolve_callback = None
    _default_callback = None
    _display_callback = None
    _fill_callback = None
    _required_callback = None
    _readonly_callback = None

    name: str = ""
    attribute: str = ""
    value = None
    resource = None

    LEFT_ALIGN = "left"
    RIGHT_ALIGN = "right"
    CENTER_ALIGN = "center"

    def __init__(self, name: str, attribute=None, resolve_callback=None):
        self.name = name
        self._resolve_callback = resolve_callback

        self.default(None)

        if callable(attribute):
            self.computed_callback = attribute
            self.attribute = "ComputedField"
        else:
            self.attribute = (
                attribute if attribute else Str.lower(name).replace(" ", "_")
            )

    def text_align(self, text_align) -> Self:
        self._text_align = text_align

        return self

    def default(self, callback) -> Self:
        self._default_callback = callback

        return self

    def resolve_for_action(self, request: DjingRequest):
        if self.value is not None:
            return

        if callable(self._default_callback):
            self._default_callback = Util.callback_with_dynamic_args(
                self._default_callback, [request]
            )

        self.value = self._default_callback

    def resolve_for_display(self, resource, attribute=None):
        try:
            self.resource = resource

            attribute = attribute if attribute else self.attribute

            if not self._display_callback:
                return self.resolve(resource, attribute)
            elif callable(self._display_callback):
                if attribute == "ComputedField":
                    self.value = Util.callback_with_dynamic_args(
                        self.computed_callback, [resource]
                    )
                else:
                    value = (
                        self.value
                        if self.value is not None
                        else self._resolve_attribute(resource, attribute)
                    )

                    self.value = value

                    self.resolve_using_display_callback(value, resource, attribute)
        except Exception as e:
            print(e)

    def resolve_using_display_callback(self, value, resource, attribute):
        self._uses_customized_display = True

        self._displayed_as = Util.callback_with_dynamic_args(
            self._display_callback, [value, resource, attribute]
        )

    def resolve(self, resource, attribute=None):
        self.resource = resource

        attribute = attribute if attribute else self.attribute

        if attribute == "ComputedField":
            self.value = Util.callback_with_dynamic_args(
                self.computed_callback, [resource]
            )
        else:
            if not self._resolve_callback:
                self.value = self._resolve_attribute(resource, attribute)
            elif callable(self._resolve_callback):
                value = self._resolve_attribute(resource, attribute)

                self.value = Util.callback_with_dynamic_args(
                    self._resolve_callback, [value, resource, attribute]
                )

    def _resolve_attribute(self, resource, attribute):
        data = value(data_get(resource, attribute)) if resource.id else None

        if isinstance(data, DeferredAttribute):
            return None

        return data

    def fill(self, request: DjingRequest, model):
        return self.fill_into(request, model, self.attribute)

    def fill_for_action(self, request: DjingRequest, model):
        return self.fill(request, model)

    def fill_into(
        self, request: DjingRequest, model, attribute, request_attribute=None
    ):
        return self.fill_attribute(
            request,
            request_attribute if request_attribute else self.attribute,
            model,
            attribute,
        )

    def fill_attribute(
        self, request: DjingRequest, request_attribute, model, attribute
    ):
        if self._fill_callback:
            return Util.callback_with_dynamic_args(
                self._fill_callback, [request, request_attribute, model, attribute]
            )

        return self.fill_attribute_from_request(
            request, request_attribute, model, attribute
        )

    def fill_attribute_from_request(
        self, request: DjingRequest, request_attribute, model, attribute
    ):
        if request_attribute in request.all():
            value = request.all().get(request_attribute)

            if value is not None:
                self.fill_model_with_data(model, value, attribute)

    def fill_model_with_data(self, model, value, attribute):
        if self.has_fillable_value(value):
            setattr(model, attribute, value)

    def has_fillable_value(self, value: Any) -> bool:
        return value is not None and value != ""

    def as_bigint(self) -> Self:
        self._is_bigint = True

        return self

    def computed(self) -> bool:
        if callable(self.attribute) or self.attribute == "ComputedField":
            return True

        return False

    def fill_using(self, callback) -> Self:
        self._fill_callback = callback

        return self

    def display_using(self, callback) -> Self:
        self._display_callback = callback

        return self

    def nullable(self, callback=True, values=None) -> Self:
        self._nullable = callback

        if values:
            self.null_values(values)

        return self

    def null_values(self, values) -> Self:
        self._null_values = values

        return self

    def is_nullable(self) -> Self:
        return self._nullable

    def sortable(self) -> Self:
        if not self.computed():
            self._sortable = True

        return self

    def sortable_uri_key(self) -> Self:
        return self.attribute

    def readonly(self, readonly_callback=True) -> Self:
        self._readonly_callback = readonly_callback

        return self

    def is_readonly(self, request: DjingRequest) -> Self:
        if self._readonly_callback == True or (
            callable(self._readonly_callback)
            and Util.callback_with_dynamic_args(self._readonly_callback, [request])
        ):
            self.set_readonly_attribute()

            return True

        return False

    def required(self, required_callback=True) -> Self:
        self._required_callback = required_callback

        return self

    def is_required(self, request: DjingRequest):
        if self._required_callback == True or (
            callable(self._required_callback)
            and Util.callback_with_dynamic_args(self._required_callback, [request])
        ):
            return True

        if self.attribute and not self._required_callback:
            if request.is_create_or_attach_request():
                creation_rules = self.get_creation_rules(request)

                return "required" in creation_rules.get(self.attribute)

            if request.is_update_or_update_attached_request():
                update_rules = self.get_update_rules(request)

                return "required" in update_rules.get(self.attribute)

        return False

    def placeholder(self, text: str) -> Self:
        self._placeholder = text

        self.with_meta({"extra_attributes": {"placeholder": text}})

        return self

    def set_readonly_attribute(self) -> Self:
        self.with_meta({"extra_attributes": {"readonly": True}})

        return self

    def show(self) -> Self:
        self._visible = True

        return self

    def hide(self) -> Self:
        self._visible = False

        return self

    def get_unique_key(self) -> str:
        attribute = self.attribute
        panel = Str.slug(self.panel if self.panel else "default")
        component = self.get_component()

        return f"{attribute}-{panel}-{component}"

    def request_should_resolve_default_value(self, request: DjingRequest):
        return request.is_create_or_attach_request() or request.is_action_request()

    def resolve_default_callback(self, request: DjingRequest):
        if not self.value and callable(self._default_callback):
            return Util.callback_with_dynamic_args(self._default_callback, [request])

        return self._default_callback

    def resolve_default_value(self, request: DjingRequest):
        if self.request_should_resolve_default_value(request):
            return self.resolve_default_callback(request)

    def has_resolvable_value(self, request: DjingRequest) -> bool:
        return self.value is not None and isinstance(
            self.value,
            (list, dict, set, tuple, str, int, float, bool, JsonSerializable),
        )

    def json_serialize(self):
        request = App.make(DjingRequest)

        meta = self.meta()

        return {
            "attribute": self.attribute,
            "component": self.get_component(),
            "displayed_as": self._displayed_as,
            "full_width": self._full_width,
            "help_text": self.get_help_text(),
            "name": self.name,
            "index_name": self.name,
            "nullable": self._nullable,
            "panel": self.panel,
            "placeholder": self._placeholder,
            "prefix_component": True,
            "readonly": self.is_readonly(request),
            "required": self.is_required(request),
            "sortable": self._sortable,
            "text_align": self._text_align,
            "unique_key": self.get_unique_key(),
            "validation_key": self.validation_key(),
            "value": (
                self.value
                if self.has_resolvable_value(request)
                else self.resolve_default_value(request)
            ),
            "visible": self._visible,
            "with_label": self._with_label,
            **meta,
        }

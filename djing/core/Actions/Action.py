from typing import TYPE_CHECKING, Self, Type
from Illuminate.Collections.helpers import value
from Illuminate.Contracts.Support.JsonSerializable import JsonSerializable
from Illuminate.Support.Facades.App import App
from Illuminate.Support.Facades.Validator import Validator
from Illuminate.Support.Str import Str
from Illuminate.Support.builtins import array_merge
from djing.core.Actions.ActionResponse import ActionResponse
from djing.core.Actions.DispatchAction import DispatchAction
from djing.core.AuthorizedToSee import AuthorizedToSee
from djing.core.Fields.FieldCollection import FieldCollection
from djing.core.Http.Requests.DjingRequest import DjingRequest
from djing.core.Makeable import Makeable
from djing.core.Metable import Metable
from djing.core.Facades.Djing import Djing
from djing.core.Resource import Resource
from django.db.models import base


if TYPE_CHECKING:
    from djing.core.Http.Requests.ActionRequest import ActionRequest


class Action(
    AuthorizedToSee,
    Makeable,
    Metable,
    JsonSerializable,
):
    FULLSCREEN_STYLE = "fullscreen"
    WINDOW_STYLE = "window"

    destructive = False
    authorized_to_run_action = None

    _name = None
    _uri_key = None
    _component = "confirm-action-modal"
    _standalone = False
    _sole = False
    _run_callback = None
    _without_confirmation = False
    _without_action_events = False

    _only_on_index = False
    _only_on_detail = False
    _show_on_index = True
    _show_on_detail = True
    _show_inline = False

    _modal_style = WINDOW_STYLE
    _modal_size = "2xl"
    _confirm_button_text = "Run Action"
    _confirm_text = "Are you sure you want to run this action?"
    _cancel_button_text = "Cancel"
    _response_type = "json"

    def sole(self) -> Self:
        self._standalone = False
        self._sole = True

        self.show_inline().show_on_detail()

        return self

    def standalone(self) -> Self:
        self._standalone = True
        self._sole = False

        return self

    def fullscreen(self) -> Self:
        self._modal_style = self.FULLSCREEN_STYLE

        return self

    def size(self, size) -> Self:
        self._modal_style = self.WINDOW_STYLE
        self._modal_size = size

        return self

    def without_confirmation(self) -> Self:
        self._without_confirmation = True

        return self

    def without_action_events(self) -> Self:
        self._without_action_events = True

        return self

    def is_standalone(self) -> bool:
        return self._standalone

    def component(self) -> str:
        return self._component

    def with_name(self, name: str) -> Self:
        self._name = name

        return self

    def name(self) -> str:
        return self._name if self._name else Djing.humanize(self)

    def uri_key(self) -> str:
        return self._uri_key if self._uri_key else Str.slug(self.name(), "-", None)

    def is_destructive(self) -> bool:
        return self.destructive

    def can_run(self, run_callback) -> Self:
        self._run_callback = run_callback

        return self

    def authorized_to_run(self, request: DjingRequest, model: base.Model) -> bool:
        authorized_to_run_action = value(
            self._run_callback if self._run_callback else True, request, model
        )

        self.authorized_to_run_action = authorized_to_run_action

        return authorized_to_run_action

    def show_inline(self) -> Self:
        self._show_inline = True

        return self

    def only_inline(self, value=True) -> Self:
        self._show_inline = value
        self._show_on_index = not value
        self._show_on_detail = not value

        return self

    def except_inline(self) -> Self:
        self._show_inline = False
        self._show_on_index = True
        self._show_on_detail = True

        return self

    def only_on_table_row(self, value=True):
        return self.only_inline(value)

    def except_on_table_row(self):
        return self.except_inline()

    def show_on_table_row(self):
        return self.show_inline()

    def shown_on_table_row(self):
        return self._show_inline

    def show_on_detail(self) -> Self:
        self._show_on_detail = True

        return self

    def only_on_detail(self, value=True) -> Self:
        self._only_on_detail = value
        self._show_on_detail = value
        self._show_on_index = not value
        self._show_inline = not value

        return self

    def except_on_detail(self) -> Self:
        self._show_on_index = True
        self._show_on_detail = False
        self._show_inline = True

        return self

    def shown_on_detail(self):
        if self._only_on_detail:
            return True

        if self._only_on_index:
            return False

        return self._show_on_detail

    def show_on_index(self) -> Self:
        self._show_on_index = True

        return self

    def only_on_index(self, value=True) -> Self:
        self._only_on_index = value
        self._show_on_index = value
        self._show_on_detail = not value
        self._show_inline = not value

        return self

    def except_on_index(self) -> Self:
        self._show_on_index = False
        self._show_on_detail = True
        self._show_inline = True

        return self

    def shown_on_index(self):
        if self._only_on_index == True:
            return True

        if self._only_on_detail:
            return False

        return self._show_on_index

    def fields(self, request: DjingRequest):
        return []

    def validate_fields(self, request: DjingRequest):
        fields = (
            FieldCollection.make(self.fields(request))
            .authorized(request)
            .without_readonly(request)
            .without_unfillable()
        )

        def get_creation_rules(fields: FieldCollection, resource: Type[Resource]):
            rules = fields.map_with_keys(
                lambda field: resource.format_rules(
                    request, field.get_creation_rules(request)
                )
            )

            return dict(rules)

        validator = Validator.make(
            request.all(), get_creation_rules(fields, request.resource())
        )

        return validator.validate()

    def handle_request(self, request: "ActionRequest"):
        fields = request.resolve_fields(request)

        dispatcher = DispatchAction(request, self, fields)

        if self._standalone:
            dispatcher.handle_standalone()
        else:
            dispatcher.handle_request()

        response = dispatcher.dispatch()

        if isinstance(response, ActionResponse):
            return response

        return ActionResponse()

    def json_serialize(self):
        request = App.make(DjingRequest)

        return array_merge(
            {
                "component": self.component(),
                "is_standalone": self.is_standalone(),
                "destructive": self.is_destructive(),
                "authorized_to_run": self.authorized_to_run_action,
                "name": self.name(),
                "uri_key": self.uri_key(),
                "fields": (
                    FieldCollection.make(self.fields(request))
                    .filter(lambda field: field and field.authorized_to_see(request))
                    .each(lambda field: field.resolve_for_action(request))
                    .values()
                    .all()
                ),
                "show_on_detail": self.shown_on_detail(),
                "show_on_index": self.shown_on_index(),
                "show_on_table_row": self.shown_on_table_row(),
                "modal_style": self._modal_style,
                "modal_size": self._modal_size,
                "cancel_button_text": self._cancel_button_text,
                "confirm_button_text": self._confirm_button_text,
                "confirm_text": self._confirm_text,
                "response_type": self._response_type,
                "without_confirmation": self._without_confirmation,
            },
            self.meta(),
        )

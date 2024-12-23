from typing import TYPE_CHECKING, Any, Callable
from Illuminate.Helpers.Util import Util
from djing.core.Fields.FieldCollection import FieldCollection

if TYPE_CHECKING:
    from djing.core.Actions.Action import Action
    from djing.core.Http.Requests.ActionRequest import ActionRequest


class DispatchAction:
    def __init__(
        self, request: "ActionRequest", action: "Action", fields: FieldCollection
    ):
        self.request = request
        self.action = action
        self.fields = fields
        self.handle_callback: Callable[..., Any] = None

    def dispatch(self):
        return self.handle_callback(self.fields)

    def _get_method(self):
        return getattr(self.action, "handle")

    def handle_standalone(self):
        self.handle_callback = lambda fields: Util.callback_with_dynamic_args(
            self._get_method(), [fields, []]
        )

    def handle_request(self):
        self.handle_callback = lambda fields: Util.callback_with_dynamic_args(
            self._get_method(), [fields, self.request.chunks(150, self.for_models)]
        )

    def for_models(self, models):
        return models

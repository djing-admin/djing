from djing.core.Fields.Password import Password
from djing.core.Http.Requests.DjingRequest import DjingRequest


class PasswordConfirmation(Password):
    component = "password-field"

    def __init__(self, name, attribute=None, resolve_callback=None):
        super().__init__(name, attribute, resolve_callback)

        self.only_on_forms()

    def fill_attribute(
        self, request: DjingRequest, request_attribute, model, attribute
    ):
        pass

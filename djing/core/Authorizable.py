from Illuminate.Exceptions.UnauthorizedAccessException import (
    UnauthorizedAccessException,
)
from Illuminate.Support.Facades.Gate import Gate
from djing.core.Http.Requests.DjingRequest import DjingRequest
from djing.core.Facades.Djing import Djing


class Authorizable:
    @classmethod
    def authorizable(cls) -> type:
        return Gate.get_policy_for(cls.new_model()) is not None

    def authorize_to_view_any(self, request: DjingRequest):
        if not self.authorizable():
            return

        gate = Gate.get_policy_for(self.new_model())

        if gate and hasattr(gate, "view_any"):
            self.authorize_to(request, "view_any")

    @classmethod
    def authorized_to_view_any(cls, request: DjingRequest):
        if not cls.authorizable():
            return True

        gate = Gate.get_policy_for(cls.new_model())

        if gate and hasattr(gate, "view_any"):
            return Gate.for_user(Djing.user(request)).check("view_any", cls.new_model())

        return True

    def authorize_to_view(self, request: DjingRequest):
        self.authorize_to(request, "view")

    def authorized_to_view(self, request: DjingRequest):
        return self.authorized_to(request, "view")

    @classmethod
    def authorize_to_create(self, request: DjingRequest):
        authorized = self.authorized_to_create(request)

        if not authorized:
            raise UnauthorizedAccessException(
                "Unauthorized: Authorizable.authorize_to_create"
            )

    @classmethod
    def authorized_to_create(cls, request: DjingRequest):
        if cls.authorizable():
            return Gate.for_user(Djing.user(request)).check("create", cls.new_model())

        return True

    def authorize_to_replicate(self, request: DjingRequest):
        if not self.authorizable():
            return True

        gate = Gate.get_policy_for(self.new_model())

        if gate and hasattr(gate, "replicate"):
            return self.authorize_to(request, "replicate")

        self.authorize_to_create(request)
        self.authorize_to_update(request)

    def authorized_to_replicate(self, request: DjingRequest):
        if not self.authorizable():
            return True

        gate = Gate.get_policy_for(self.new_model())

        if gate and hasattr(gate, "replicate"):
            return Gate.for_user(Djing.user(request)).check("replicate", self.model())

        return self.authorized_to_create(request) and self.authorized_to_update(request)

    def authorize_to_update(self, request: DjingRequest):
        self.authorize_to(request, "update")

    def authorized_to_update(self, request: DjingRequest):
        return self.authorized_to(request, "update")

    def authorize_to_delete(self, request: DjingRequest):
        self.authorize_to(request, "delete")

    def authorized_to_delete(self, request: DjingRequest):
        return self.authorized_to(request, "delete")

    def authorized_to_restore(self, request: DjingRequest):
        return self.authorized_to(request, "restore")

    def authorized_to_force_delete(self, request: DjingRequest):
        return self.authorized_to(request, "force_delete")

    def authorize_to(self, request: DjingRequest, ability):
        if self.authorizable():
            Gate.for_user(Djing.user(request)).authorize(ability, self.resource)

    def authorized_to(self, request: DjingRequest, ability):
        if self.authorizable():
            return Gate.for_user(Djing.user(request)).check(ability, self.resource)

        return True

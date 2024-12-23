from abc import abstractmethod
from typing import Any
from Illuminate.Helpers.Util import Util
from Illuminate.Support.Str import Str
from Illuminate.Support.builtins import array_merge
from django.db.models import Model, QuerySet
from djing.core.Card import Card
from djing.core.Facades.Djing import Djing
from djing.core.Http.Requests.DjingRequest import DjingRequest
from djing.core.Metrics.HasHelpText import HasHelpText


class Metric(Card, HasHelpText):
    _name = None
    _only_on_detail = False

    def resolve(self, request: DjingRequest):
        resolver = self.get_resolver(request)

        return resolver()

    def only_on_detail(self):
        self._only_on_detail = True

        return self

    def name(self) -> str:
        return self._name if self._name else Djing.humanize(self)

    def uri_key(self) -> str:
        return Str.slug(self.name(), "-", None)

    def key(self):
        return f"{self.__module__}.{self.__class__.__name__}"

    def get_resolver(self, request: DjingRequest):
        if self._only_on_detail:
            return lambda: Util.callback_with_dynamic_args(
                self.calculate, [request, request.find_model_or_fail()]
            )

        return lambda: Util.callback_with_dynamic_args(self.calculate, [request, None])

    @abstractmethod
    def calculate(self, request: DjingRequest, model: Any = None):
        raise NotImplementedError("Not Implemented")

    def json_serialize(self):
        return array_merge(
            super().json_serialize(),
            {
                "class": self.key(),
                "name": self._name,
                "uri_key": self.uri_key(),
                "help_width": self._help_width,
                "help_text": self._help_text,
            },
        )

    def _get_queryset(self, request: DjingRequest, model: Model | Any) -> QuerySet:
        assert model is not None, "model is required"

        if issubclass(model, Model):
            return model.objects.get_queryset()

        if isinstance(model, Model):
            resource_class = request.new_resource_with(model)

            return resource_class.new_query()

        raise Exception("Invalid Model")

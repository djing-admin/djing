from typing import Any, Callable
from djing.core.Events.ServingDjing import ServingDjing
from Illuminate.Support.Facades.Event import Event
from djing.core.Events.DjingServiceProviderRegistered import (
    DjingServiceProviderRegistered,
)


class InteractsWithEvents:
    @classmethod
    def booted(cls, callback: Callable[[Any], Any]):
        Event.listen(DjingServiceProviderRegistered, callback)

    @classmethod
    def serving(cls, callback: Callable[[Any], Any]):
        Event.listen(ServingDjing, callback)

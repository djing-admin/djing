from Illuminate.Foundation.Events.Dispatchable import Dispatchable
from djing.core.Http.Requests.DjingRequest import DjingRequest


class ServingDjing(Dispatchable):
    def __init__(self, request: DjingRequest):
        self.request = request

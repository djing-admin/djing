from djing.core.Http.Requests.CardRequest import CardRequest
from djing.core.Http.Requests.InteractsWithLenses import InteractsWithLenses


class LensCardRequest(InteractsWithLenses, CardRequest):
    request_name = "LensCardRequest"

    def available_cards(self):
        return self.lens().available_cards(self)

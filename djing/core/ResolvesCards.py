from Illuminate.Collections.helpers import collect
from djing.core.Http.Requests.DjingRequest import DjingRequest


class ResolvesCards:
    def available_cards(self, request: DjingRequest):
        return (
            self.resolve_cards(request)
            .filter(lambda card: card._only_on_detail == False)
            .filter(lambda card: card.authorize(request))
            .values()
        )

    def available_cards_for_detail(self, request: DjingRequest):
        return (
            self.resolve_cards(request)
            .filter(lambda card: card._only_on_detail == True)
            .filter(lambda card: card.authorize(request))
            .values()
        )

    def resolve_cards(self, request: DjingRequest):
        return collect(self.cards(request))

    def cards(self, request: DjingRequest):
        return []

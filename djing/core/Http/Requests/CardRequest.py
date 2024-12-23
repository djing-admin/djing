from djing.core.Http.Requests.DjingRequest import DjingRequest


class CardRequest(DjingRequest):
    def available_cards(self):
        new_resource = self.new_resource()

        if self.query_param("resource_id"):
            return new_resource.available_cards_for_detail(self)

        return new_resource.available_cards(self)

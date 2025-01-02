from abc import abstractmethod


class FilterableField:
    @abstractmethod
    def apply_filter(self, request, query, value):
        raise NotImplementedError("Not Implmented")

    @abstractmethod
    def resolve_filter(self, request):
        raise NotImplementedError("Not Implmented")

    @abstractmethod
    def serialize_for_filter(self):
        raise NotImplementedError("Not Implmented")

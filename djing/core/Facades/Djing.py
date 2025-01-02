from Illuminate.Support.Facades.Facade import Facade


class Djing(metaclass=Facade):
    @classmethod
    def get_facade_accessor(cls):
        return "djing"

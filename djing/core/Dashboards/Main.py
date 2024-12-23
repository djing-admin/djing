from Illuminate.Support.Str import Str
from djing.core.Cards.Help import Help
from djing.core.Dashboard import Dashboard


class Main(Dashboard):
    def name(self):
        return self.__class__.__name__

    def uri_key(self):
        return Str.snake(self.__class__.__name__)

    def cards(self):
        return [
            Help(),
        ]

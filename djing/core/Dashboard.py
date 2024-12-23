from Illuminate.Support.Str import Str
from djing.core.AuthorizedToSee import AuthorizedToSee
from djing.core.Http.Requests.DjingRequest import DjingRequest
from djing.core.Element import Element
from djing.core.Facades.Djing import Djing
from djing.core.HasMenu import HasMenu
from djing.core.Makeable import Makeable
from djing.core.Menu.MenuItem import MenuItem


class Dashboard(Element, AuthorizedToSee, Makeable, HasMenu):
    _name = None
    _show_refresh_button = False

    def name(self):
        return self._name if self._name else Djing.humanize(self)

    def label(self):
        return self.name()

    def uri_key(self):
        return Str.singular(Str.snake(self.__name__, "-"))

    def menu(self, request: DjingRequest):
        return MenuItem.dashboard(self.__class__)

    def show_refresh_button(self):
        self._show_refresh_button = True

        return self

from typing import Self
from Illuminate.Support.builtins import array_merge
from djing.core.Fields.Number import Number
from babel.numbers import get_currency_symbol, format_currency, get_currency_precision

from djing.core.Http.Requests.DjingRequest import DjingRequest


class Currency(Number):
    component = "currency-field"

    _currency_symbol = None
    _currency = "USD"
    _locale = "en"
    _minor_units = False

    def __init__(self, name, attribute=None, resolve_callback=None):
        super().__init__(name, attribute, resolve_callback)

        self._currency_symbol = get_currency_symbol(self._currency, self._locale)

        (
            self.step(self.get_step_value())
            .fill_using(self.fill_value)
            .display_using(self.format_money)
        )

    def get_step_value(self) -> float:
        decimal_places = get_currency_precision(self._currency)

        step_value = 1 / (10**decimal_places)

        return step_value

    def fill_value(self, request: DjingRequest, request_attribute, model, attribute):
        if request_attribute in request.all():
            value = request.all().get(request_attribute)

            if self.has_fillable_value(value):
                if self._minor_units:
                    new_value = self.format_money_without_symbol(value)

                    setattr(model, attribute, new_value)
                else:
                    setattr(model, attribute, value)

    def format_money(self, value) -> str | None:
        if value is None:
            return None

        return format_currency(
            number=value,
            currency=self._currency,
            locale=self._locale,
        )

    def format_money_without_symbol(self, value) -> float:
        value = self.format_money(value)

        return float(value.replace(self._currency_symbol, ""))

    def currency(self, currency) -> Self:
        self._currency = currency

        self._currency_symbol = get_currency_symbol(
            currency=self._currency,
            locale=self._locale,
        )

        return self

    def locale(self, locale) -> Self:
        self._locale = locale

        self._currency_symbol = get_currency_symbol(
            currency=self._currency,
            locale=self._locale,
        )

        return self

    def symbol(self, currency_symbol) -> Self:
        self._currency_symbol = currency_symbol

        return self

    def as_minor_units(self) -> Self:
        self._minor_units = True

        return self

    def resolve_currency_symbol(self):
        if self._currency_symbol:
            return self._currency_symbol

        return get_currency_symbol(self._currency, self._locale)

    def json_serialize(self):
        return array_merge(
            super().json_serialize(),
            {
                "currency": self.resolve_currency_symbol(),
            },
        )

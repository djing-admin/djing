from djing.core.Contracts.FilterableField import FilterableField
from djing.core.Fields.Field import Field
from djing.core.Fields.FieldFilterable import FieldFilterable
from djing.core.Fields.Unfillable import Unfillable


class Badge(Field, FieldFilterable, FilterableField, Unfillable):
    pass

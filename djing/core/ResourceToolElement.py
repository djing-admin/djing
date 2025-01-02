from djing.core.Fields.FieldElement import FieldElement


class ResourceToolElement(FieldElement):
    def __init__(self, component=None):
        super().__init__(component)

        self.only_on_detail()

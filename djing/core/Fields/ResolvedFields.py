from Illuminate.Collections.Collection import Collection


class ResolvedFields(Collection):
    def __init__(self, attributes: Collection, callbacks: Collection):
        super().__init__(attributes)

        self.callbacks = callbacks

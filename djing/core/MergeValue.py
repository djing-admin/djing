from Illuminate.Collections.Collection import Collection


class MergeValue:
    def __init__(self, data):
        if isinstance(data, Collection):
            self.data = data.all()
        else:
            self.data = data

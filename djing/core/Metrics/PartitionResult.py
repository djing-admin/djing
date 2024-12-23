from Illuminate.Contracts.Support.JsonSerializable import JsonSerializable


class PartitionResult(JsonSerializable):
    def __init__(self, value, total, group_by_column, label_callback):
        self._value = value
        self._total = total
        self._group_by_column = group_by_column
        self._label_callback = label_callback

    def json_serialize(self):
        value = [
            {
                "label": self._label_callback(result[self._group_by_column]),
                "value": result["data"],
                "percent": round(result["data"] / self._total * 100, 2),
            }
            for result in self._value
        ]

        return {"value": value, "total": self._total}

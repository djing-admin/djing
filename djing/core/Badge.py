from Illuminate.Contracts.Support.JsonSerializable import JsonSerializable


class Badge(JsonSerializable):
    def json_serialize(self):
        return {}

import base64
import json


class FilterEncoder:
    def __init__(self, filters=[]):
        self._filters = filters

    def encode(self):
        filter_string = json.dumps(self._filters).encode("utf-8")

        return base64.b64encode(filter_string).decode("utf-8")

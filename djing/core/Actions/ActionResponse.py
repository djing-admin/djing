from typing import Self
from Illuminate.Contracts.Support.JsonSerializable import JsonSerializable


class ActionResponse(JsonSerializable):
    def __init__(self, data=None):
        self.data = data or {
            "response_type": "message",
            "data": {
                "type": "success",
                "message": "The action was executed successfully.",
            },
        }

    @classmethod
    def success(cls, message) -> Self:
        data = {
            "response_type": "message",
            "data": {
                "type": "success",
                "message": message,
            },
        }

        return cls(data)

    @classmethod
    def danger(cls, message) -> Self:
        data = {
            "response_type": "message",
            "data": {
                "type": "danger",
                "message": message,
            },
        }

        return cls(data)

    @classmethod
    def redirect(cls, url) -> Self:
        data = {
            "response_type": "redirect",
            "data": {
                "url": url,
                "open_in_new_tab": False,
                "remote": True,
            },
        }

        return cls(data)

    @classmethod
    def open_in_new_tab(cls, url) -> Self:
        data = {
            "response_type": "redirect",
            "data": {
                "url": url,
                "open_in_new_tab": True,
                "remote": True,
            },
        }

        return cls(data)

    @classmethod
    def visit(cls, url) -> Self:
        data = {
            "response_type": "redirect",
            "data": {
                "url": url,
                "open_in_new_tab": False,
                "remote": False,
            },
        }

        return cls(data)

    def json_serialize(self):
        return self.data

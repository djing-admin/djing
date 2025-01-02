from typing import Self
from Illuminate.Contracts.Support.JsonSerializable import JsonSerializable
from Illuminate.Support.Facades.App import App
from djing.core.Facades.Djing import Djing
from djing.core.Makeable import Makeable


class URL(Makeable, JsonSerializable):
    def __init__(self, url, remote=False):
        if isinstance(url, URL):
            self._url = url._url
            self._remote = url._remote

        self._url = url
        self._remote = remote

    @classmethod
    def remote(cls, url) -> Self:
        return cls(url, True)

    def get(self):
        return self._url if self._remote else Djing.url(self._url)

    def __str__(self):
        return self.get()

    def active(self):
        request = App.make("request")

        url = self.get()

        return request.get_url() == url

    def json_serialize(self):
        return {
            "url": self._url,
            "remote": self._remote,
        }

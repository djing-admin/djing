from abc import abstractmethod


class HandleRoutes:
    @classmethod
    @abstractmethod
    def path(cls) -> str:
        raise NotImplementedError("Not Implemented")

    @classmethod
    def url(cls, url: str) -> str:
        path = cls.path().rstrip("/")

        if url and isinstance(url, str):
            url = url.strip("/")

            return f"{path}/{url}"

        return "/"

from abc import abstractmethod


class Previewable:
    @abstractmethod
    def preview_for(self, value: str) -> str:
        raise NotImplementedError("Not Implemented")

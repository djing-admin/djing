from abc import abstractmethod


class BehavesAsPanel:
    @abstractmethod
    def as_panel(self):
        raise NotImplementedError("Not Implemented")

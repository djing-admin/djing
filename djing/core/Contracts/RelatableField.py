from abc import abstractmethod


class RelatableField:
    @abstractmethod
    def relationship_name(self):
        raise NotImplementedError("Not Implemented")

    @abstractmethod
    def relationship_type(self):
        raise NotImplementedError("Not Implemented")

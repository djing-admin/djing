from abc import abstractmethod


class Storable:
    @abstractmethod
    def get_storage_disk(self):
        raise NotImplementedError("Not Implemented")

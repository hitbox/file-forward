from abc import ABC
from abc import abstractmethod

class ClientBase(ABC):

    @abstractmethod
    def read(self, *args):
        pass

    @abstractmethod
    def listdir(self, path=None):
        pass

    @property
    @abstractmethod
    def name(self):
        pass

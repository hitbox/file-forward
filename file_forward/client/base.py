from abc import ABC
from abc import abstractmethod

class ClientBase(ABC):

    @abstractmethod
    def normalize_path(self, path):
        pass

    @abstractmethod
    def read(self, *args):
        pass

    @abstractmethod
    def listdir(self, path=None):
        pass

    @abstractmethod
    def move(self, src, dst):
        pass

    @abstractmethod
    def exists(self, path):
        pass

    @abstractmethod
    def makedirs(self, path):
        pass

    @abstractmethod
    def stat(self, path):
        pass

    @property
    @abstractmethod
    def name(self):
        pass

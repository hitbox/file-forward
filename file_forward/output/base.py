from abc import ABC
from abc import abstractmethod

class OutputBase(ABC):

    @abstractmethod
    def __call__(self, source_result):
        """
        Write output from source result object.
        """

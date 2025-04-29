from abc import ABC
from abc import abstractmethod

class ScanBase(ABC):
    """
    Scan ABC class.
    """

    def __iter__(self):
        yield from self.generate_results()

    @abstractmethod
    def generate_results(self):
        """
        Generate SourceResult objects for file listing.
        """

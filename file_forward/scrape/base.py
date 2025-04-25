from abc import ABC
from abc import abstractmethod

class ScrapeBase(ABC):

    @abstractmethod
    def __call__(self, data):
        """
        Scrape the bytes data and return a dict.
        """

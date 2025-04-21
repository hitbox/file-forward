from abc import ABC
from abc import abstractmethod

class ArchiveBase(ABC):

    def __contains__(self, value):
        return self.contains(value)

    @abstractmethod
    def contains(self, source_result):
        """
        Return if the archive has already seen this file.
        """

    @abstractmethod
    def add(self, source_result):
        """
        Record this source as contained in the archive.
        """

    @abstractmethod
    def save(self):
        """
        Commit archive to long term storage.
        """

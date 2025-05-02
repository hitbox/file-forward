import os

from abc import ABC
from abc import abstractmethod

class ArchiveBase(ABC):
    """
    Base class for objects that check and commit files to an archive, to avoid
    processing again.
    """

    def __contains__(self, value):
        return self.contains(value)

    def _log_exception(self, logger, source_result, exc):
        filename = os.path.basename(source_result.path)
        logger.exception('Exception on %s: %s', filename, exc)

    def _log_repeat_exception(self, logger, source_result, exc):
        filename = os.path.basename(source_result.path)
        logger.debug('Repeated failure for %s', filename)

    @abstractmethod
    def handle_exception(self, source_result, exc):
        """
        Archive an exception during file processing.
        """

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

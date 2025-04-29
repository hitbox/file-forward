import logging
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

    def handle_exception(self, source_result, exc):
        """
        Archive an exception during file processing.
        """
        filename = os.path.basename(source_result.path)
        if filename in self._exceptions:
            log_meth = self._log_repeat_exception
        else:
            # Give concrete class opportunity to do something.
            self._exception(source_result, exc)
            log_meth = self._log_exception

        log_meth(self.logger, source_result, exc)

    @property
    def logger(self):
        """
        """
        if hasattr(self, '_logger'):
            return self._logger
        try:
            # Use concrete class's module name for logger name.
            return logging.getLogger(self.__module__)
        except KeyError:
            raise RuntimeError('No logger found in instance or globals.')

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

    @abstractmethod
    def _exception(self, source_result, exc):
        """
        Concrete class's chance to do something with the exceptional source_result.
        """

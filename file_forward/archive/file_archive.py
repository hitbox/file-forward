import os

from .base import ArchiveBase

class FileArchive(ArchiveBase):
    """
    Save paths to a line separated file.
    """

    def __init__(self, success_fn, exception_fn):
        """
        :param success_fn: Path to save filenames to.
        """
        self.success_fn = success_fn
        self.exception_fn = exception_fn
        self._successes = self._load(self.success_fn)
        self._exceptions = self._load(self.exception_fn)

    def _load(self, filename):
        archive = set()
        if filename is not None and os.path.exists(filename):
            with open(filename, 'r') as file:
                for line in file:
                    archive.add(line.strip())
        return archive

    def _save(self, filename, archive):
        if filename is not None:
            with open(filename, 'w') as file:
                file.write('\n'.join(archive))

    def contains(self, source_result):
        return os.path.normpath(source_result.path) in self._successes

    def add(self, source_result):
        self._successes.add(os.path.normpath(source_result.path))

    def save(self):
        """
        Save in-memory archive to storage.
        """
        self._save(self.success_fn, self._successes)
        self._save(self.exception_fn, self._exceptions)

    def handle_exception(self, source_result, exc):
        self._exceptions.add(source_result.filename)

from .base import ArchiveBase

class NullArchive(ArchiveBase):
    """
    The never archived archive.
    """

    def __init__(self):
        self._exceptions = set()

    def contains(self, source_result):
        return False

    def add(self, source_result):
        pass

    def save(self):
        pass

    def _exception(self, source_result, exc):
        pass

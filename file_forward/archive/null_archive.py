from .base import ArchiveBase

class NullArchive(ArchiveBase):
    """
    The never archived archive.
    """

    def contains(self, source_result):
        return False

    def add(self, source_result):
        pass

    def save(self):
        pass

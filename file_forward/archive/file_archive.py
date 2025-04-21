import os

from .base import ArchiveBase

class FileArchive(ArchiveBase):
    """
    Save paths to a line separated file.
    """

    def __init__(self, filename):
        """
        :param filename: Path to save filenames to.
        """
        self.filename = filename
        self._archive = self._load_archive()

    def _load_archive(self):
        if not os.path.exists(self.filename):
            archive = set()
        else:
            with open(self.filename, 'r') as archive_file:
                archive = set(line.strip() for line in archive_file)
        return archive

    def contains(self, source_result):
        return os.path.normpath(source_result.path) in self._archive

    def add(self, source_result):
        self._archive.add(os.path.normpath(source_result.path))

    def save(self):
        """
        Save in-memory archive to storage.
        """
        with open(self.filename, 'w') as archive_file:
            archive_file.write('\n'.join(self._archive))

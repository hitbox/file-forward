import logging

from itertools import count

from .base import ArchiveBase

logger = logging.getLogger(__name__)

class MoveToArchive(ArchiveBase):
    """
    Move file to archive it.
    """

    def __init__(
        self,
        client,
        success_dest,
        path_module,
        rename_for_exists = False,
    ):
        self.client = client
        self.success_dest = success_dest
        self.path_module = path_module
        self.rename_for_exists = rename_for_exists
        self._moves = []

    def contains(self, source_result):
        """
        Always return False, assuming the move worked and was not returned by
        file listing.
        """
        return False

    def _destination(self, directory, source_result):
        """
        Return directory for destination from source_result and string.
        """
        directory = str(directory).format(**source_result.path_data)
        return self.path_module.join(directory, source_result.filename)

    def handle_exception(self, source_result, exc):
        """
        Move source for exception to another directory and write a traceback
        next to it, with a .traceback extension.
        """

    def add(self, source_result):
        """
        Add successful archive item.
        """
        self._moves.append((source_result, self.success_dest, None))

    def save(self):
        """
        Move files to archive.
        """
        with self.client as client:
            for source_result, dstfmt, exc in self._moves:
                # Source path.
                src = source_result.path

                # Resolve destination from format string.
                dst = self._destination(dstfmt, source_result)

                # Handle existing destination path.
                if client.exists(dst):
                    # Raise if not renaming.
                    if not self.rename_for_exists:
                        raise FileExistsError(f'{dst} already exists.')

                    # Insert integer before extension to make destination unique.
                    for number in count(1):
                        root, ext = self.path_module.splitext(dst)
                        candidate = f'{root}.{number}{ext}'

                        if not client.exists(candidate):
                            dst = candidate
                            logger.debug('destination renamed:%s', dst)
                            break

                # Move file to archive.
                client.move(src, dst)

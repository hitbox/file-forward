import logging
import os
import shutil

from itertools import count

import file_forward.path

from .base import ArchiveBase

logger = logging.getLogger(__name__)

class MoveToArchive(ArchiveBase):
    """
    Move file to archive it.
    """

    def __init__(self, client, success_dest, exception_dest=None, rename_for_exists=False):
        self.client = client
        self.success_dest = success_dest
        self.exception_dest = exception_dest
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
        return os.path.join(directory, source_result.filename)

    def handle_exception(self, source_result, exc):
        """
        Move source for exception to another directory and write a traceback
        next to it, with a .traceback extension.
        """
        self._moves.append((source_result, self.exception_dest, exc))

    def add(self, source_result):
        """
        Add successful archive item.
        """
        self._moves.append((source_result, self.success_dest, None))

    def save(self):
        """
        Move files to archive.
        """
        for source_result, dstfmt, exc in self._moves:
            # Source path.
            src = source_result.path

            # Resolve destination from format string.
            dst = self._destination(dstfmt, source_result)

            # Handle existing destination path.
            if self.client.exists(dst):
                # Raise if not renaming.
                if not self.rename_for_exists:
                    raise FileExistsError(f'{dst} already exists.')

                # Insert integer to make destination unique.
                for number in count(1):
                    candidate = insert_before_ext(dst, f'.{number}')
                    if not self.client.exists(candidate):
                        dst = candidate

            self.client.move(src, dst)

            if exc and self.exception_dest:
                # Write traceback for exception.
                tb_dst = self._destination(self.exception_dest, source_result)
                with open(tb_dst + '.traceback', 'w', encoding='utf8') as traceback_file:
                    traceback_file.write(exc)

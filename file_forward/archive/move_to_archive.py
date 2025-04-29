import os
import shutil

import file_forward.path

from .base import ArchiveBase

class MoveToArchive(ArchiveBase):
    """
    Move file to archive it.
    """

    def __init__(self, success_dest, exception_dest, rename_for_exists=False):
        self.success_dest = success_dest
        self.exception_dest = exception_dest
        self.rename_for_exists = rename_for_exists

    def contains(self, source_result):
        """
        Always return False, assuming the move worked.
        """
        return False

    def _destination(self, directory, source_result):
        """
        Return directory for destination from source_result and string.
        """
        directory = str(directory).format(**source_result.path_data)
        return os.path.join(directory, source_result.filename)

    def _move(self, src, dst):
        """
        Move file renaming for exists, if configured.
        """
        if os.path.exists(dst):
            # Raise if not renaming.
            if not self.rename_for_exists:
                raise FileExistsError(f'{dst} already exists.')

            # Insert integer to make destination unique.
            dst = file_forward.path.rename_unique(dst)

        shutil.move(src, dst)

    def add(self, source_result):
        """
        Move file to destination.
        """
        dest = self._destination(self.success_dest, source_result)
        self._move(source_result.path, dest)

    def save(self):
        """
        Does nothing, we do the work on `add`.
        """

    def _exception(self, source_result, exc):
        """
        Move source for exception to another directory and write a traceback
        next to it, with a .traceback extension.
        """
        dest = self._destination(self.exception_dest, source_result)
        self._move(source_result.path, dest)
        with open(dest + '.traceback', 'w', encoding='utf8') as traceback_file:
            traceback_file.write(exc)

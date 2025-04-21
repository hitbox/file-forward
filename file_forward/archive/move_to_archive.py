import os
import shutil

import file_forward.path

from .base import ArchiveBase

class MoveToArchive(ArchiveBase):
    """
    Move file to archive it.
    """

    def __init__(self, destination, rename_for_exists=False):
        self.destination = destination
        self.rename_for_exists = rename_for_exists

    def contains(self, source_result):
        """
        Always return False, assuming the move worked.
        """
        return False

    def add(self, source_result, metadata):
        """
        Move file to destination.
        """
        dest_path = os.path.join(
            # Just sketching things out here.
            str(self.destination).format(**metadata),
            # This is problem. The source path will be a full path.
            source_result.path,
        )

        if os.path.exists(dest_path):
            # Raise if not renaming.
            if not self.rename_for_exists:
                raise FileExistsError(f'{dest_path} already exists.')

            # Insert integer to make destination unique.
            dest_path = file_forward.path.rename_unique(dest_path)

        shutil.move(source_result.path, dest_path)

    def save(self):
        """
        Does nothing, we do the work on `add`.
        """

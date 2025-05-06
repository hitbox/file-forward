import os

from .base import OutputBase

class FileOutput(OutputBase):
    """
    Write in-memory file data to a real file.
    """

    def __init__(self, filename):
        self.filename = filename

    def __call__(self, file):
        # Allow format string from source file data.
        context = file.flat_dict()
        filename = self.filename.format(**context)

        # Ensure directory structure is available.
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        # Write saved file data to file system.
        with open(filename, 'wb') as output_file:
            output_file.write(file.file_data)

        # Update copy to mirror stat()
        stat_data = file.stat_data
        times = (stat_data.st_atime, stat_data.st_mtime)
        os.utime(filename, times)

    def finalize(self):
        """
        Nothing to do, this is not an accumulator.
        """

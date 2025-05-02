import os

from file_forward.util import strict_update
from file_forward.util import writer

from .base import OutputBase

class FileOutput(OutputBase):

    def __init__(self, filename, stream=None):
        self.filename = filename
        self.stream = stream

    def __call__(self, source_result):
        context = source_result.flat_dict()
        strict_update(context, {'path': source_result.path})
        filename = self.filename.format(**context)

        os.makedirs(os.path.dirname(filename), exist_ok=True)

        with open(filename, 'wb') as output_file:
            output_file.write(source_result.file_data)

        stat_data = source_result.stat_data
        times = (stat_data.st_atime, stat_data.st_mtime)
        os.utime(filename, times)

    def finalize(self):
        """
        Nothing to do.
        """

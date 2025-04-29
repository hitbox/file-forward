import os

from collections import namedtuple
from pprint import pformat

from file_forward.util import normalize_path
from file_forward.util import zip_bytes

class SourceResult(
    namedtuple(
        'SourceResult',
        field_names = [
            'client',
            'path',
            'path_data',
            'file_data',
            'posix',
        ],
        defaults = [
            False, # posix
        ]
    ),
):
    """
    Consistent object for result of source objects.
    """

    @property
    def normalized_fullpath(self):
        return normalize_path(self.path, self.posix)

    @property
    def directory(self):
        return normalize_path(self.directory, self.posix)

    @property
    def filename(self):
        return normalize_path(os.path.basename(self.path), self.posix)

    def _asdict(self):
        # TODO
        # - Add more data for context to output classes.
        return super()._asdict()

    def ppstring(self):
        return pformat([self.directory, self.filename, self.path_data])

    def zip_file_data(self):
        return zip_bytes(self.file_data, self.filename)

    def log_entry(self):
        return f'{self.client.name}:{self.normalized_fullpath}'

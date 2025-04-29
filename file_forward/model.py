import os

from pprint import pformat

from file_forward.lido import LCBMessage
from file_forward.util import normalize_path
from file_forward.util import zip_bytes

class SourceResult:
    """
    Consistent object for result of source objects.
    """

    def __init__(self, client, path, path_data, file_data, posix=False):
        self.client = client
        self.path = path
        self.path_data = path_data
        self.file_data = file_data
        self.posix = posix

    @property
    def normalized_fullpath(self):
        return normalize_path(self.path, posix=self.posix)

    def ppstring(self):
        directory = normalize_path(self.directory, self.posix)
        filename = normalize_path(self.filename, self.posix)
        return pformat([directory, filename, self.path_data])

    def zip_file_data(self):
        filename = os.path.basename(self.path)
        return zip_bytes(self.file_data, filename)

    def as_lcb_message(self):
        return LCBMessage.from_source_result(self)

    def log_entry(self):
        return f'{self.client.name}:{self.normalized_fullpath}'

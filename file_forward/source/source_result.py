import os

from pprint import pformat

from file_forward.lido import LCBMessage
from file_forward.util import normalize_path
from file_forward.util import zip_bytes

class SourceResult:
    """
    Consistent object for result of source objects.
    """

    def __init__(self, filename, directory, path_data, file_data, posix=False):
        self.filename = filename
        self.directory = directory
        self.path_data = path_data
        self.file_data = file_data
        self.posix = posix

    @property
    def fullpath(self):
        return os.path.join(self.directory, self.filename)

    @property
    def normalized_fullpath(self):
        return normalize_path(self.fullpath, posix=self.posix)

    def ppstring(self):
        directory = normalize_path(self.directory, self.posix)
        filename = normalize_path(self.filename, self.posix)
        return pformat([directory, filename, self.path_data])

    def zip_file_data(self):
        return zip_bytes(self.file_data, self.filename)

    def as_lcb_message(self):
        return LCBMessage.from_source_result(self)

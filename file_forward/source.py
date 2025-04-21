import os
import re

from abc import ABC
from abc import abstractmethod
from pprint import pformat

class SourceResult:
    """
    Consistent object for result of source objects.
    """

    def __init__(self, filename, directory, path_data, file_data):
        self.filename = filename
        self.directory = directory
        self.path_data = path_data
        self.file_data = file_data

    def ppstring(self):
        return '\n'.join([self.directory, self.filename, pformat(self.path_data)])


class SourceBase(ABC):
    """
    Source ABC class.
    """

    def __iter__(self):
        yield from self.generate_results()

    @abstractmethod
    def generate_results(self):
        """
        Generate SourceResult objects for file listing.
        """


class PatternSource(SourceBase):
    """
    Match and parse regex against files in directory.
    """

    def __init__(self, pattern, root_dir, schema):
        self.pattern = pattern
        self.root_dir = root_dir
        self.schema = schema

    def generate_results(self):
        filename_re = re.compile(self.pattern)
        for filename in os.listdir(self.root_dir):
            path = os.path.join(self.root_dir, filename)
            match = filename_re.match(filename)
            if match:
                if self.schema:
                    path_data = self.schema(match.groupdict())
                else:
                    path_data = {}
                with open(path, 'rb') as path_file:
                    file_data = path_file.read()
                yield SourceResult(filename, self.root_dir, path_data, file_data)


class SFTPGlob(SourceBase):
    """
    Iterator of paths matching regex on SFTP.
    """

    def __init__(self, sftp, pattern, root_dir, schema):
        """
        :param hostname:
            Server to connect to, required.
        """
        self.sftp_params = sftp
        self.pattern = pattern
        self.root_dir = root_dir
        self.schema = schema

    def generate_results(self):
        filename_re = re.compile(self.pattern)
        with sftp_connect(**self.sftp_params) as sftp:
            sftp.chdir(self.root_dir)
            for filename in sftp.listdir():
                path = os.path.join(self.root_dir, filename)
                match = filename_re.match(filename)
                if match:
                    path_data = self.schema(match.groupdict())
                    # TODO: read file into memory
                    file_data = None
                    yield SourceResult(filename, self.root_dir, path_data, file_data)

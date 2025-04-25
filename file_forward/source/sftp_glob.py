import logging
import os
import re

from file_forward.sftp import sftp_connect

from .base import SourceBase
from .source_result import SourceResult

logger = logging.getLogger(__name__)

class SFTPGlob(SourceBase):
    """
    Iterator of paths matching regex on SFTP.
    """

    def __init__(self, sftp, pattern, root_dir, schema, posix=True):
        """
        :param hostname:
            Server to connect to, required.
        """
        self.sftp_params = sftp
        self.pattern = pattern
        self.root_dir = root_dir
        self.schema = schema
        self.posix = posix

    def generate_results(self):
        filename_re = re.compile(self.pattern)
        with sftp_connect(**self.sftp_params) as sftp:
            sftp.chdir(self.root_dir)
            for filename in sftp.listdir():
                path = os.path.join(self.root_dir, filename)
                match = filename_re.match(filename)
                if match:
                    # Scrape data from path filename.
                    path_data = self.schema(match.groupdict())
                    # Read data into memory.
                    with sftp.open(path, 'rb') as remote_file:
                        file_data = remote_file.read()
                    source_result = SourceResult(filename, self.root_dir, path_data, file_data, posix)
                    logger.info('sftp:%s', path)
                    yield source_result

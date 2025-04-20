import os
import re

class PatternSource:

    def __init__(self, pattern, root_dir, schema):
        self.pattern = pattern
        self.root_dir = root_dir
        self.schema = schema

    def run(self):
        filename_re = re.compile(self.pattern)
        for filename in os.listdir(self.root_dir):
            path = os.path.join(self.root_dir, filename)
            match = filename_re.match(filename)
            if match:
                data = self.schema(match.groupdict())
                yield (path, data)


class SFTPGlob:
    """
    Iterator of paths on SFTP.
    """

    def __init__(self, sftp, pattern, root_dir):
        """
        :param hostname:
            Server to connect to, required.
        """
        self.sftp_params = sftp
        self.pattern = pattern
        self.root_dir = root_dir

    def run(self):
        filename_re = re.compile(self.pattern)
        with sftp_connect(**self.sftp_params) as sftp:
            sftp.chdir(self.root_dir)
            for filename in sftp.listdir():
                path = os.path.join(self.root_dir, filename)
                match = filename_re.match(filename)
                if match:
                    yield (path, match)

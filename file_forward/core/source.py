import fnmatch
import os
import re

from contextlib import contextmanager

import paramiko

class PatternSource:
    """
    List files from dir that match a pattern.
    """
    # TODO
    # - schema probably does not belong here.

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

@contextmanager
def sftp_connect(host, port, username, password):
    transport = paramiko.Transport((host, port))
    try:
        transport.connect(username=username, password=password)
        sftp = paramiko.SFTPClient.from_transport(transport)
        yield sftp
    finally:
        sftp.close()
        transport.close()

def sftp_walk(sftp, base_path, pattern):
    try:
        files = sftp.listdir_attr(base_path)
    except Exception:
        return []

    matched = []
    for file in files:
        path = f'{base_path}/{file.filename}'

        if S_ISDIR(file.st_mode):
            matched.extend(sftp_walk(sftp, path, pattern))

        if fnmatch.fnmatch(file.filename, pattern):
            matched.append(path)

    return matched

def S_ISDIR(mode):
    """
    Check if mode of file is directory.
    S_ISDIR
    """
    return (mode & 0o170000) == 0o040000

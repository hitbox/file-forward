import argparse
import configparser
import inspect
import os

from contextlib import contextmanager

import paramiko

CONFIG_VAR = 'FILE_FORWARD_CONFIG'

class SFTPGlob:
    """
    Iterator of paths on SFTP.
    """

    def __init__(self, sftp, glob):
        """
        :param hostname:
            Server to connect to, required.
        """
        self.sftp_params = sftp
        self.glob_params = glob

    def __iter__(self):
        pass


@contextmanager
def sftp_connect(host, post, username, password):
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
    # S_ISDIR
    return (mode & 0o170000) == 0o040000

def run(args, cp):
    """
    Select unprocessed files from a source and send them to a queue.
    """
    pass

def config_from_args(args):
    """
    Return config parser from command line arguments.
    """
    cp = configparser.ConfigParser()
    # Read optional environment variable.
    cp.read(os.environ.get(CONFIG_VAR))
    # Read from command line arguments.
    cp.read(args.config)
    return cp

def main(argv=None):
    parser = argparse.ArgumentParser(
        description = run.__doc__,
    )
    parser.add_argument(
        '--config',
        action = 'append',
        default = [],
        help =
            'Configuration files. Environment variable'
            f' {CONFIG_VAR} is also loaded.',
    )
    args = parser.parse_args(argv)

    cp = config_from_args(args)
    print(dict(cp))

if __name__ == '__main__':
    main()

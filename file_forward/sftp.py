import fnmatch

from contextlib import contextmanager

import paramiko

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

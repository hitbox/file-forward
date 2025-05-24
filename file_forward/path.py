import os

from itertools import count

app_dir = os.path.dirname(__file__)
project_dir = os.path.dirname(app_dir)
instance_dir = os.path.join(project_dir, 'instance')

archive_dir = os.path.join(instance_dir, 'archive')
certs_dir = os.path.join(instance_dir, 'certs')
etc_dir = os.path.join(instance_dir, 'etc')
logging_dir = os.path.join(instance_dir, 'logging')

def insert_before_ext(path, substring):
    """
    Insert a string, usually an integer, just before the extension.
    """
    root, ext = os.path.splitext(path)
    return f'{root}{substring}{ext}'

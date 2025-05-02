import os

from itertools import count

app_dir = os.path.dirname(__file__)
project_dir = os.path.dirname(app_dir)
instance_dir = os.path.join(project_dir, 'instance')
archive_dir = os.path.join(instance_dir, 'archive')
etc_dir = os.path.join(instance_dir, 'etc')
certs_dir = os.path.join(instance_dir, 'certs')

def rename_unique(path, sep='.'):
    """
    Rename file with integers until not found.
    """
    original = path
    for number in count(1):
        candidate = insert_before_ext(original, number, sep)
        if not os.path.exists(candidate):
            return candidate

def insert_before_ext(path, index, sep):
    """
    Insert a string, usually an integer, just before the extension.
    """
    root, ext = os.path.splitext(path)
    return f'{root}{sep}{index}{ext}'

def insert_before_ext(path, substring):
    root, ext = os.path.splitext(path)
    return f'{root}{substring}{ext}'

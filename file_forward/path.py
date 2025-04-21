import os

from itertools import count

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

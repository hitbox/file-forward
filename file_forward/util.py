import binascii
import io
import operator
import sys
import zipfile

from functools import reduce
from pathlib import Path

def bitwise_or(*args):
    """
    Return the bitwise OR of the arguments.
    """
    return reduce(operator.or_, args)

def decode_md(md):
    """
    Return a dict of an IBM MQ message descriptor.
    """
    result = {}
    for attr in dir(md):
        if attr.startswith('_') or callable(getattr(md, attr)):
            continue
        value = getattr(md, attr)
        if isinstance(value, bytes):
            try:
                value = value.decode('utf-8').strip('\x00')
            except UnicodeDecodeError:
                # fallback: show as hex string
                value = binascii.hexlify(value).decode('ascii')
        result[attr] = value
    return result

def normalize_path(path, posix=False):
    if posix:
        return str(Path(path).as_posix())
    else:
        return str(Path(path).resolve())

def strict_update(d1, d2):
    """
    Strictly update dict d1 from d2, raising for existing keys.
    """
    overlap = set(d1).intersection(d2)
    if overlap:
        raise KeyError(f'Attempted overwrite keys {overlap}')
    d1.update(d2)

def writer(target):
    if target == 'stdout':
        return sys.stdout
    elif target == 'stderr' or target is None:
        return sys.stderr
    elif hasattr(target, 'write'):
        return target
    else:
        return open(target, 'w')

def zip_bytes(input_bytes, filename):
    """
    Archive input_bytes in a ZIP with filename, in memory.
    """
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zf:
        zf.writestr(filename, input_bytes)
    return zip_buffer.getvalue()

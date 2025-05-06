import binascii
import importlib.util
import io
import os
import sys
import zipfile

from itertools import groupby
from operator import itemgetter
from pathlib import Path

import pymqi

from sqlalchemy import or_

from .constant import LEG_IDENTIFIER_KEYS
from .constant import OFP_VERSION_KEYS

leg_identifier_key = itemgetter(*LEG_IDENTIFIER_KEYS)
ofp_version_key = itemgetter(*OFP_VERSION_KEYS)

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

def get_pythonw_path():
    python_dir = os.path.dirname(sys.executable)
    pythonw = os.path.join(python_dir, 'pythonw.exe')
    if os.path.exists(pythonw):
        return pythonw

def grouped(iterable, key=None):
    """
    Convenience to sort and group with one function.
    """
    return groupby(sorted(iterable, key=key), key=key)

def max_in_group(iterable, groupkey=None, newkey=None):
    """
    Generate newest items in iterable from groupings.
    """
    for key, groupiter in grouped(iterable, key=groupkey):
        yield max(groupiter, key=newkey)

def invert_dict(d, strict=False):
    """
    Invert keys and values for dict d. If strict, raise for duplicate
    value-keys.
    """
    inverted = {}
    for key, val in d.items():
        if strict and val in inverted:
            raise ValueError(f'Duplicate key for value {val}')
        inverted[val] = key
    return inverted

def is_one(*args, null=None):
    """
    Exactly one arg in args is not in the null set.
    """
    if not isinstance(null, (list, set, tuple)):
        null = [null]
    else:
        null = list(set(null))
    return sum(arg not in null for arg in args) == 1

def jsonable(obj):
    """
    Return obj ready for JSON.
    """
    if isinstance(obj, (str, int, float, bool)) or obj is None:
        return obj
    elif isinstance(obj, (list, set, tuple)):
        return [jsonable(item) for item in obj]
    elif isinstance(obj, dict):
        return {jsonable(key): jsonable(val) for key, val in obj.items()}
    elif hasattr(obj, '__dict__'):
        return {
            key: jsonable(val)
            for key, val in obj.__dict__.items()
            if not key.startswith('_') and not callable(val)
        }
    else:
        return str(obj)

def load_pyfile(path):
    """
    Load Python file.
    """
    module_name, _ = os.path.splitext(os.path.basename(path))
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def message_with_properties(queue_manager, properties):
    """
    Create MQ message with properties from dict.
    """
    # MessageHandle holds the message properties
    message_handle = pymqi.MessageHandle(queue_manager)

    # Set message properties from LCBMessage fields.
    for key, val in properties.items():
        if val is not None:
            key = key.encode()
            message_handle.properties.set(key, val)

    put_message_options = pymqi.PMO(
        Version = pymqi.CMQC.MQPMO_VERSION_3, # PMO v3 is required
    )
    put_message_options.OriginalMsgHandle = message_handle.msg_handle

    message_descriptor = pymqi.MD(
        Version = pymqi.CMQC.MQMD_CURRENT_VERSION,
    )

    return (message_descriptor, put_message_options)

def normalize_path(path, posix=False):
    """
    Normalize path to POSIX style or absolute OS-native style.
    """
    if posix:
        return str(Path(path).as_posix())
    else:
        return str(Path(path).resolve())

def posix_parts(path):
    return path.strip('/').split('/')

def strict_update(d1, d2):
    """
    Strictly update dict d1 from d2, raising for existing keys.
    """
    overlap = set(d1).intersection(d2)
    if overlap:
        raise KeyError(f'Attempted overwrite keys {overlap}')
    d1.update(d2)

def writer(target):
    """
    Resolve target name to a writable stream.
    """
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

def raise_for_empty_string(key, value):
    if not value or not value.strip():
        raise ValueError(f'{key} must be a non-empty string.')
    return value

def is_overlapping(
    session,
    model_class,
    left_id_name,
    right_id_name,
    valid_from_name,
    valid_to_name,
    left_id,
    right_id,
    new_from,
    new_to = None,
):
    left_id_col = getattr(model_class, left_id_name)
    right_id_col = getattr(model_class, right_id_name)
    valid_from_col = getattr(model_class, valid_from_name)
    valid_to_col = getattr(model_class, valid_to_name)

    overlap = session.query(model_class).where(
        # Rows matching the ids
        left_id_col == left_id,
        right_id_col == right_id,
        # And, either valid_to is None, or new_to is None, or new_to is less than or equal to valid_from
        or_(
            valid_to_col == None,
            new_to is None,
            valid_from_col <= new_to,
        ),
        # And, either new_to is None, or valid_to is None, or new_from is less than or equal to the valid_to
        or_(
            new_to is None,
            valid_to_col == None,
            new_from <= valid_to_col
        ),
    )
    return session.query(overlap.exists()).scalar()

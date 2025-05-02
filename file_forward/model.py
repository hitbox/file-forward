import os

from collections import namedtuple
from operator import itemgetter
from pprint import pformat

from file_forward.constant import LEG_IDENTIFIER_KEYS
from file_forward.util import normalize_path
from file_forward.util import strict_update
from file_forward.util import zip_bytes

leg_identifier = itemgetter(*LEG_IDENTIFIER_KEYS)

class SourceResult(
    namedtuple(
        'SourceResult',
        field_names = [
            'client',
            'path',
            'path_data',
            'file_data',
            'stat_data',
            'posix',
        ],
        defaults = [
            False, # posix
        ]
    ),
):
    """
    Consistent object for result of source objects.
    """

    @property
    def normalized_fullpath(self):
        return normalize_path(self.path, self.posix)

    @property
    def directory(self):
        return normalize_path(self.directory, self.posix)

    @property
    def filename(self):
        return normalize_path(os.path.basename(self.path), self.posix)

    @property
    def client_name(self):
        return self.client.name

    @property
    def leg_identifier(self):
        return leg_identifier(self.path_data)

    @property
    def ofp_version(self):
        return self.path_data.get('ofp_version')

    def ppstring(self):
        return pformat([self.directory, self.filename, self.path_data])

    def zip_file_data(self):
        return zip_bytes(self.file_data, self.filename)

    def log_entry(self):
        return f'{self.client.name}:{self.normalized_fullpath}'

    def flat_dict(self):
        data = {
            'client_name': self.client_name,
            'normalized_fullpath': self.normalized_fullpath,
        }
        strict_update(data, self.path_data)
        return data


class OFPVersion(
    namedtuple(
        'OFPVersion',
        field_names = [
            'ofp_version_major',
            'ofp_version_minor',
            'ofp_version_patch',
        ],
        defaults = [
            0,
            0,
            0,
        ],
    ),
):
    """
    Named tuple of the three parts of an OFP version--the major, minor, and patch integers.
    """


class Rowifier:
    """
    List of dicts to rows for Excel formatting hints through class names.
    """

    def __init__(self, header, include_header=True, formatters=None):
        """
        :param header:
            The order of keys to get from the dicts.
        :param include_header:
            Include a header row in generated output.
        :param formatters:
            Dict of keys to callables to format values.
        """
        self.header = header
        self.include_header = include_header
        self.formatters = {} if formatters is None else formatters

    def __call__(self, rows):
        if self.include_header:
            values = tuple(self.header)
            classes = set(['header'])
            yield (values, classes)

        # Pass-through value (no formatter).
        pass_value = lambda value: value

        # Formatter for key or pass-through.
        formatter = lambda key: self.formatters.get(key, pass_value)

        for row_data in rows:
            values = tuple(formatter(key)(row_data[key]) for key in self.header)
            classes = set(['data'])
            yield (values, classes)

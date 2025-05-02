import marshmallow as mm

from marshmallow.fields import Date
from marshmallow.fields import String

from file_forward.constant import DEFAULT_OPERATIONAL_SUFFIX

class TupleField(mm.fields.Field):
    """
    Split a separated string into a fixed-length tuple, converting parts to a
    given type.
    """

    def __init__(self, sep, fill, length, type=int, dump_sep=None, **kwargs):
        """
        :param sep: Separator character.
        :param fill: Character or integer for filling until length is reached.
        :param length: Integer length to make final tuple.
        :param type: Callable converts parts to this type.
        """
        super().__init__(**kwargs)
        self.sep = sep
        self.fill = fill
        self.length = length
        self.type = type
        self.dump_sep = dump_sep

    def _deserialize(self, value, attr, data, **kwargs):
        parts = value.split(self.sep)
        parts += [self.fill] * (self.length - len(parts))
        if len(parts) > self.length:
            raise mm.ValidationError(
                f'Expected length {self.length}, got {len(parts)}.')
        return tuple(map(self.type, parts))

    def _serialize(self, value, attr, obj, **kwargs):
        sep = self.dump_sep or self.sep
        return sep.join(map(str, value))


def flight_date_field(data_key):
    return Date(
        data_key = data_key,
        format = '%d%b%y',
    )

def ofp_version_field(**kwargs):
    kwargs.setdefault('sep', '_')
    kwargs.setdefault('fill', 0)
    kwargs.setdefault('length', 3)
    kwargs.setdefault('dump_sep', '.')

    ofp_version = TupleField(**kwargs)
    return ofp_version

def operational_suffix_field():
    return String(
        load_default = DEFAULT_OPERATIONAL_SUFFIX,
        dump_default = DEFAULT_OPERATIONAL_SUFFIX,
    )

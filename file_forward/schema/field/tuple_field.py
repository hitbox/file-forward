from marshmallow import ValidationError
from marshmallow.fields import Field

class TupleField(Field):
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
            raise ValidationError(
                f'Expected length {self.length}, got {len(parts)}.')
        return tuple(map(self.type, parts))

    def _serialize(self, value, attr, obj, **kwargs):
        sep = self.dump_sep or self.sep
        return sep.join(map(str, value))

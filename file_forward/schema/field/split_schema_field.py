from marshmallow import ValidationError
from marshmallow.fields import Field

class SplitSchemaField(Field):
    """
    Split a string on a separator for values, combine with names for keys, and
    process further with a schema.
    """

    def __init__(self, separator, keys, schema_class, dump_sep=None, **kwargs):
        """
        :param separator: Separator character.
        """
        super().__init__(**kwargs)
        self.separator = separator
        self.keys = keys
        self.schema_class = schema_class
        self.dump_sep = dump_sep

    def _deserialize(self, value, attr, data, **kwargs):
        data = dict(zip(self.keys, value.split(self.separator)))
        schema = self.schema_class()
        return schema.load(data)

    def _serialize(self, value, attr, obj, **kwargs):
        separator = self.dump_sep or self.separator
        return separator.join(map(str, value))

from marshmallow import ValidationError
from marshmallow.fields import Date
from marshmallow.fields import Field
from marshmallow.fields import String

from file_forward.constant import DEFAULT_OPERATIONAL_SUFFIX

from .split_schema_field import SplitSchemaField
from .tuple_field import TupleField

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

from marshmallow import Schema
from marshmallow.fields import DateTime
from marshmallow.fields import Integer
from marshmallow.fields import String

from .field import flight_date_field
from .field import ofp_version_field
from .field import operational_suffix_field

class DataMixin:

    airline_icao = String()
    flight_number = String()
    flight_date = flight_date_field('flight_date_string')

    ofp_version = ofp_version_field(load_default=(0, 0, 0))
    operational_suffix = operational_suffix_field()


class LogLineMixin:
    """
    """

    datetime = DateTime()
    level_name = String()
    level_integer = Integer()
    logger_name = String()
    message = String()

import marshmallow as mm

from marshmallow import Schema
from marshmallow import post_load
from marshmallow.fields import Integer
from marshmallow.fields import String
from marshmallow.fields import Time

from file_forward.model import OFPVersion
from file_forward.util import strict_update

from .field import flight_date_field
from .field import ofp_version_field
from .field import operational_suffix_field

class DataMixin:

    airline_icao = String()
    flight_number = String()
    flight_date = flight_date_field('flight_date_string')

    ofp_version = ofp_version_field(load_default=(0, 0, 0))
    operational_suffix = operational_suffix_field()

from marshmallow import Schema
from marshmallow import post_load
from marshmallow import validate
from marshmallow.fields import Date
from marshmallow.fields import DateTime
from marshmallow.fields import Integer
from marshmallow.fields import List
from marshmallow.fields import Nested
from marshmallow.fields import String
from marshmallow.fields import Time

from .mixin import LogLineMixin

class DataSchema(Schema):

    aircraft_registration = String()
    airline_icao = String()
    block_in_time = Time()
    block_off_time = Time()
    departure_icao = String()
    destination_icao = String()
    flight_date_string = Date(format='%d%b%y')
    flight_number = String()
    ofp_version = String()
    take_off_weight_pounds = Integer()


class ScanScrapeSchema(LogLineMixin, Schema):

    data = Nested(DataSchema)

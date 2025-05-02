import marshmallow as mm

from marshmallow import Schema
from marshmallow import post_load
from marshmallow.fields import String

from file_forward.model import OFPVersion
from file_forward.util import strict_update

from .field import flight_date_field
from .field import ofp_version_field
from .field import operational_suffix_field

class ASMFilenameSchema(Schema):
    """
    Ad-hoc Scheduled Message filename schema.
    """

    airline_icao = String()
    flight_number = String()
    number1 = String()
    flight_date = flight_date_field('flight_date_string')
    time1 = String()
    time2 = String()
    departure_iata = String()
    destination_iata = String()
    aircraft_registration = String(load_default='')

    ofp_version = ofp_version_field(load_default=(0, 0, 0))

    operational_suffix = operational_suffix_field()

    def __init__(self, airline_mapper, **kwargs):
        super().__init__(**kwargs)
        self.airline_mapper = airline_mapper

    @post_load
    def add_extra_keys(self, data, **kwargs):
        """
        Add keys expected by LegIdentifierField.
        """
        data['airline_iata'] = self.airline_mapper.iata(data['airline_icao'])
        # Add empty ofp version structure fields.
        strict_update(data, OFPVersion()._asdict())
        return data

import marshmallow as mm

from marshmallow import Schema
from marshmallow import post_load
from marshmallow.fields import String

from file_forward.model import OFPVersion
from file_forward.util import strict_update

from .field import TupleField
from .field import flight_date_field
from .field import ofp_version_field
from .field import operational_suffix_field

class OptiClimbFilenameSchema(Schema):
    """
    OptiClimb filename schema.
    """

    airline_icao = String()
    flight_number = String()
    flight_date = flight_date_field('flight_date_string')
    departure_icao = String()
    destination_icao = String()
    operational_suffix = operational_suffix_field()
    aircraft_registration = String()

    ofp_version = ofp_version_field(data_key='ofp_string')

    def __init__(self, airline_mapper, airport_mapper, **kwargs):
        super().__init__(**kwargs)
        self.airline_mapper = airline_mapper
        self.airport_mapper = airport_mapper

    @post_load
    def add_extra_keys(self, data, **kwargs):
        """
        Add keys expected by LegIdentifierField.
        """
        data['airline_iata'] = self.airline_mapper.iata(data['airline_icao'])
        data['departure_iata'] = self.airport_mapper.iata(data['departure_icao'])
        data['destination_iata'] = self.airport_mapper.iata(data['destination_icao'])

        # Provide separated OFP version fields.
        ofp_version = OFPVersion(*data['ofp_version'])
        strict_update(data, ofp_version._asdict())
        return data

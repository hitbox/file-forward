import marshmallow as mm

from marshmallow import Schema
from marshmallow import post_load
from marshmallow.fields import Integer
from marshmallow.fields import String
from marshmallow.fields import Time

from file_forward.model import OFPVersion
from file_forward.util import strict_update

from .field import TupleField
from .field import flight_date_field
from .field import ofp_version_field
from .field import operational_suffix_field
from .mixin import DataMixin

class OptiClimbFilenameSchema(DataMixin, Schema):
    """
    OptiClimb filename schema.
    """

    departure_icao = String()
    destination_icao = String()
    aircraft_registration = String()

    take_off_weight_pounds = Integer()
    block_off_time = Time()
    block_in_time = Time()

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

from marshmallow import Schema
from marshmallow import post_load
from marshmallow.fields import Integer
from marshmallow.fields import String
from marshmallow.fields import Time

from file_forward.model import OFPVersion
from file_forward.util import strict_update

from .mixin import DataMixin

class ASMFilenameSchema(DataMixin, Schema):
    """
    Ad-hoc Scheduled Message filename schema.
    """

    number1 = String()
    time1 = String()
    time2 = String()

    departure_iata = String()
    destination_iata = String()
    aircraft_registration = String(load_default='')

    take_off_weight_pounds = Integer(load_default=None)
    block_off_time = Time(load_default=None)
    block_in_time = Time(load_default=None)

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

import marshmallow as mm

from marshmallow import Schema
from marshmallow import post_load
from marshmallow.fields import String

from .field import flight_date_field

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

    def __init__(self, airline_mapper, **kwargs):
        super().__init__(**kwargs)
        self.airline_mapper = airline_mapper

    @post_load
    def add_extra_keys(self, data, **kwargs):
        data['airline_iata'] = self.airline_mapper.iata(data['airline_icao'])
        return data

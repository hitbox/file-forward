import string

from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Time
from sqlalchemy import select
from sqlalchemy.orm import relationship
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy

from .base import Base
from .mixin import UIMixin

class LegIdentifierModel(Base, UIMixin):
    """
    Uniquely identify a flight leg and some extra information.
    """

    __tablename__ = 'leg_identifier'

    __ui_meta__ = {
        'airline_iata': {
            'label': 'Airline',
            'td_attrs': {
                'class': 'data',
            },
        },
        'flight_number': {
            'label': 'Flight',
            'td_attrs': {
                'class': 'data',
            },
        },
        'flight_date': {
            'label': 'Date',
            'formatter': lambda date: date.strftime('%d%b%y'),
            'td_attrs': {
                'class': 'data',
            },
        },
        'departure_iata': {
            'label': 'Dept.',
            'td_attrs': {
                'class': 'data',
            },
        },
        'destination_iata': {
            'label': 'Dest.',
            'td_attrs': {
                'class': 'data',
            },
        },
        'take_off_weight': {
            'label': 'TOW',
            'formatter': lambda take_off_weight: f'{take_off_weight:,}',
            'td_attrs': {
                'class': 'data',
            },
        },
        'block_in_time': {
            'label': 'Blk. In',
            'formatter': lambda block_in: block_in.strftime('%H:%M'),
            'td_attrs': {
                'class': 'data',
            },
        },
        'block_off_time': {
            'label': 'Blk. Off',
            'formatter': lambda block_in: block_in.strftime('%H:%M'),
            'td_attrs': {
                'class': 'data',
            },
        },
    }

    id = Column(Integer, primary_key=True)

    airline_id = Column(ForeignKey('airline.id'))
    airline = relationship(
        'Airline',
        back_populates = 'leg_identifiers',
    )

    airline_iata = association_proxy(
        'airline',
        'code_iata',
        info = {
            'label': 'Airline',
        },
    )

    airline_icao = association_proxy('airline', 'code_icao')

    flight_number = Column(
        String,
        nullable = False,
        info = {
            'label': 'Flight',
        },
    )

    flight_date = Column(
        Date,
        nullable = False,
        info = {
            'label': 'Date',
        },
    )

    departure_id = Column(Integer, ForeignKey('airport.id'))
    departure = relationship(
        'Airport',
        foreign_keys = [departure_id],
        back_populates = 'departure_leg_identifiers',
    )
    departure_iata = association_proxy(
        'departure',
        'code_iata',
        info = {
            'label': 'Dept.',
        },
    )
    departure_icao = association_proxy('departure', 'code_icao')

    destination_id = Column(Integer, ForeignKey('airport.id'))
    destination = relationship(
        'Airport',
        foreign_keys = [destination_id],
        back_populates = 'destination_leg_identifiers',
    )
    destination_iata = association_proxy(
        'destination',
        'code_iata',
        info = {
            'label': 'Dest.',
        },
    )
    destination_icao = association_proxy('destination', 'code_icao')

    operational_suffix = Column(String(1), nullable=False)

    take_off_weight = Column(Integer, nullable=False)

    block_in_time = Column(Time, nullable=False)
    block_off_time = Column(Time, nullable=False)

    ofp_version = Column(String, nullable=False)

    @property
    def take_off_weight_display(self):
        return f'{self.take_off_weight:,}'

    @property
    def block_in_time_display(self):
        return self.block_in_time.strftime('%H:%M')

    @property
    def block_off_time_display(self):
        return self.block_off_time.strftime('%H:%M')

    @property
    def flight_date_display(self):
        return f'{self.flight_date:%d%b%y}'

    @classmethod
    def from_leg_identifier_field(cls, leg_identifier_field):
        """
        Instantiate LegIdentifierModel from MQ message LegIdentifierField object.
        """
        from .airline import Airline
        from .airport import Airport
        from file_forward import context

        session = context.get_session_context()
        extra_data = context.extra_data.get()

        airline = Airline.one_by_iata(session, leg_identifier_field.airline_code)
        departure = Airport.one_by_iata(session, leg_identifier_field.departure_airport)
        destination = Airport.one_by_iata(session, leg_identifier_field.destination_airport)

        ofp_version = '.'.join(map(str, extra_data['ofp_version']))

        instance = cls(
            airline = airline,
            flight_number = leg_identifier_field.flight_number,
            flight_date = leg_identifier_field.date_of_origin,
            departure = departure,
            destination = destination,
            operational_suffix = leg_identifier_field.operational_suffix,
            take_off_weight = extra_data['take_off_weight_pounds'],
            block_in_time = extra_data['block_in_time'],
            block_off_time = extra_data['block_off_time'],
            ofp_version = ofp_version,
        )
        return instance

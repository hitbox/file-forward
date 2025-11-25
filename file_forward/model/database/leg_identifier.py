import string

from datetime import datetime

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

from file_forward.model.lido.leg_identifier_field import DATE_OF_ORIGIN_FORMAT
from file_forward.model.lido.leg_identifier_field import LegIdentifierField

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

    aircraft_registration_id = Column(
        Integer,
        ForeignKey('aircraft_registration.id'),
        nullable = False,
    )

    aircraft_registration = relationship(
        'AircraftRegistration',
    )

    departure_id = Column(
        Integer,
        ForeignKey('airport.id'),
        nullable = False,
    )

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

    destination_id = Column(
        Integer,
        ForeignKey('airport.id'),
        nullable = False,
    )

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

    operational_suffix = Column(String(1), nullable=True)

    take_off_weight = Column(Integer, nullable=True, doc='Take off weight in pounds.')

    block_in_time = Column(Time, nullable=True)

    block_off_time = Column(Time, nullable=True)

    ofp_version = Column(String, nullable=True)

    def flattened(self):
        # Method to behave like:
        # ofpfeed.models.capture.database.Capture.flattened
        data = {
            'id': self.id,
            'process_name': 'file_forward.from_logs',
            'source_filename': None,
            'output_filename': None,
            'aircraft_registration': self.aircraft_registration.aircraft_registration,
            'flight_origin_date': self.flight_date,
            # Added to be compatible with the ofpfeed project.
            'flight_origin_date_typed': self.flight_date,
            'airline_iata': self.airline_iata,
            'airline_icao': self.airline_icao,
            'flight_number': self.flight_number,
            'origin_iata': self.departure_iata,
            'origin_icao': self.departure_icao,
            'destination_iata': self.destination_iata,
            'destination_icao': self.destination_icao,
        }
        return data

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

    @classmethod
    def from_leg_identifier_string(
        cls,
        session,
        leg_identifier_string,
        aircraft_registration_object,
    ):
        """
        LegIdentifierModel instance from dot separated leg identifier string as
        from the legIdentifier string in MQ LCB messages.
        """
        # The original motivation for this method is creating
        # LegIdentifierModel instances from log lines.
        from .airline import Airline
        from .airport import Airport

        leg_identifier_field = LegIdentifierField.from_string(leg_identifier_string)

        airline_object = Airline.one_by_iata(session, leg_identifier_field.airline_code)
        departure_object = Airport.one_by_iata(session, leg_identifier_field.departure_airport)
        destination_object = Airport.one_by_iata(session, leg_identifier_field.destination_airport)

        session.add_all([airline_object, departure_object, destination_object])

        instance = cls(
            airline = airline_object,
            flight_number = leg_identifier_field.flight_number,
            flight_date = leg_identifier_field.date_of_origin,
            departure = departure_object,
            destination = destination_object,
            operational_suffix = leg_identifier_field.operational_suffix,
            aircraft_registration = aircraft_registration_object,
        )
        return instance

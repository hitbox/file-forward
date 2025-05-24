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

from .base import Base

class LegIdentifierModel(Base):
    """
    Uniquely identify a flight leg and some extra information.
    """

    __tablename__ = 'leg_identifier'

    id = Column(Integer, primary_key=True)

    airline_id = Column(ForeignKey('airline.id'))
    airline = relationship('Airline', back_populates='leg_identifiers')

    flight_number = Column(String, nullable=False)
    flight_date = Column(Date, nullable=False)

    departure_id = Column(Integer, ForeignKey('airport.id'))
    departure = relationship(
        'Airport',
        foreign_keys = [departure_id],
        back_populates = 'departure_leg_identifiers',
    )

    destination_id = Column(Integer, ForeignKey('airport.id'))
    destination = relationship(
        'Airport',
        foreign_keys = [destination_id],
        back_populates = 'destination_leg_identifiers',
    )

    operational_suffix = Column(String(1), nullable=False)

    take_off_weight = Column(Integer, nullable=False)

    block_in_time = Column(Time, nullable=False)
    block_off_time = Column(Time, nullable=False)

    # Not part of the leg identifier in my original.
    #ofp_version_id = Column(ForeignKey('ofp_version.id'))
    #ofp_version = relationship('OFPVersion')

    @classmethod
    def from_leg_identifier_field(cls, leg_identifier_field):
        """
        """
        from .airline import Airline
        from .airport import Airport
        from file_forward import context

        session = context.get_session_context()
        extra_data = context.extra_data.get()

        airline = Airline.one_by_iata(session, leg_identifier_field.airline_code)
        departure = Airport.one_by_iata(session, leg_identifier_field.departure_airport)
        destination = Airport.one_by_iata(session, leg_identifier_field.destination_airport)

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
        )
        return instance

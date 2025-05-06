import string

from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Time
from sqlalchemy.orm import relationship
from sqlalchemy.orm import validates

from .base import Base

class LegIdentifier(Base):

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

    @validates('operational_suffix')
    def validate_operational_suffix(self, key, value):
        if value not in ' ' + string.uppercase_ascii:
            raise ValueError(f'{key} must be a space or uppercase alphabet character.')
        return value

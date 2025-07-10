from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import validates

from .base import Base

class LCBMessageFilter(Base):
    """
    Values to allow LCB messages to be sent.
    """

    __tablename__ = 'lcb_message_filter'

    id = Column(
        Integer,
        primary_key = True,
    )

    airline_code = Column(
        String,
        nullable = False,
        doc = 'IATA airline code.',
    )

    date_of_origin = Column(
        Date,
        nullable = False,
    )

    flight_number = Column(
        String,
        nullable = False,
    )

    departure_airport = Column(
        String,
        nullable = False,
        doc = 'IATA departure airport code.',
    )

    destination_airport = Column(
        String,
        nullable = False,
        doc = 'IATA destination airport code.',
    )

    def as_data_dict(self):
        """
        Return dict of filter values without the id primary key.
        """
        return {
            'airline_code': self.airline_code,
            'date_of_origin': self.date_of_origin,
            'flight_number': self.flight_number,
            'departure_airport': self.departure_airport,
            'destination_airport': self.destination_airport,
        }

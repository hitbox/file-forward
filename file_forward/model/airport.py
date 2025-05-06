from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Time
from sqlalchemy.orm import relationship
from sqlalchemy.orm import validates

from file_forward.util import raise_for_empty_string

from .base import Base
from .mixin import CodePairMixin

class Airport(CodePairMixin, Base):

    __tablename__ = 'airport'

    id = Column(Integer, primary_key=True)

    departure_leg_identifiers = relationship(
        'LegIdentifier',
        foreign_keys = 'LegIdentifier.departure_id',
        back_populates='departure',
    )

    destination_leg_identifiers = relationship(
        'LegIdentifier',
        foreign_keys = 'LegIdentifier.destination_id',
        back_populates='destination',
    )

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy.orm import relationship

from .base import Base
from .mixin import CodePairMixin

class Airport(CodePairMixin, Base):

    __tablename__ = 'airport'

    id = Column(Integer, primary_key=True)

    departure_leg_identifiers = relationship(
        'LegIdentifierModel',
        foreign_keys = 'LegIdentifierModel.departure_id',
        back_populates='departure',
    )

    destination_leg_identifiers = relationship(
        'LegIdentifierModel',
        foreign_keys = 'LegIdentifierModel.destination_id',
        back_populates='destination',
    )

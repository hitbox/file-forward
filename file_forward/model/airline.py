from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy.orm import relationship

from .base import Base
from .mixin import CodePairMixin

class Airline(CodePairMixin, Base):

    __tablename__ = 'airline'

    id = Column(Integer, primary_key=True)

    leg_identifiers = relationship('LegIdentifierModel', back_populates='airline')

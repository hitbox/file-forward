from sqlalchemy import CheckConstraint
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship
from sqlalchemy.orm import validates

from file_forward.util import raise_for_empty_string

from .base import Base
from .mixin import CodePairMixin

class Airline(CodePairMixin, Base):

    __tablename__ = 'airline'

    id = Column(Integer, primary_key=True)

    leg_identifiers = relationship('LegIdentifier', back_populates='airline')

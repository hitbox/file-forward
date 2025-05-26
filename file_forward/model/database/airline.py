from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy.orm import relationship

from .base import Base
from .mixin import CodePairMixin
from .mixin import UIMixin

class Airline(CodePairMixin, UIMixin, Base):
    """
    IATA and ICAO airline codes.
    """

    __tablename__ = 'airline'

    __ui_meta__ = {
        'code_iata': {
            'label': 'IATA',
            'td_attrs': {
                'class': 'data',
            },
        },
        'code_icao': {
            'label': 'ICAO',
            'td_attrs': {
                'class': 'data',
            },
        },
    }

    id = Column(Integer, primary_key=True)

    leg_identifiers = relationship('LegIdentifierModel', back_populates='airline')

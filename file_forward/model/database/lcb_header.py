from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship

from .base import Base

class LCBHeaderModel(Base):
    """
    Header part of LCB message.
    """

    __tablename__ = 'lcb_header'

    __ui_meta__ = {
        'jms_type': {
            'label': 'JMS Type',
        },
        'jms_expiration': {
            'label': 'JMS Expiration',
        },
    }

    id = Column(Integer, primary_key=True)

    jms_type = Column(String, nullable=False)

    jms_expiration = Column(
        Integer,
        nullable = True,
        doc =
            'Contains message’s expiration timestamp in milliseconds.'
            ' Default expiration is set to 24h. Sample: 1546344000000',
    )

    lcb_message = relationship(
        'LCBMessageModel',
        back_populates = 'lcb_header',
    )
